# Title: shared roadway problem
# Description: Write a simple threaded program where the threads are
# cars and they have to share a road they can change directions based
# on user input.

import threading
from time import *

def drive(direction):
    global express
    # driveing down the road
    # check to see if gate is open
    while True:
        if express.isopen(direction):
            print('Driver taking express lanes going {0}'.format(direction))
            sleep(5)
            express.exit()

class expressLane():
    direction = 'north'
    gates = {'north': 0, 'south': 1}
    count = 0
    lock = threading.Lock()

    def isopen(self, direction):
        self.lock.acquire()
        try:
            if self.direction == direction:
                self._enter()
                return True
        finally:
            self.lock.release()
        # check direction
        return False

    def switch(self, direction):
        self.lock.acquire()
        print('switch: got lock')
        try:
            if direction == 'south':
                self.close('north')
                print('closing north')
            if direction == 'north':
                self.close('south')
                print('closing south')

            # wait for lanes to clear
            while self.count > 0:
                print('waiting for cars to exit')
                sleep(2)

            if direction == 'south':
                self.direction = 'south'
                self.open('south')
            elif direction == 'north':
                self.direction = 'north'
                self.open('north')
        finally:
            self.lock.release()

    def _enter(self):
        self.count += 1

    def exit(self):
        if self.count > 0:
            self.count -= 1

    def close(self, gate=None):
        if gate == None:
            self.gates['north'] = 0
            self.gates['south'] = 0
        elif gate == 'north':
            self.gates['north'] = 0
        elif gate == 'south':
            self.gates['south'] = 0

    def open(self, gate=None):
        if gate == None:
            self.gates['north'] = 1
            self.gates['south'] = 1
        elif gate == 'north':
            self.gates['north'] = 1
        elif gate == 'south':
            self.gates['south'] = 1

if __name__ == '__main__':
    norththreads = []
    souththreads = []
    express = expressLane()

    for n in range(1):
        t = threading.Thread(target=drive, args=('north',))
        t.start()
        norththreads.append(t)

    for n in range(1):
        t = threading.Thread(target=drive, args=('south',))
        t.start()
        souththreads.append(t)


    while True:
        userInput = raw_input()
        # north or south
        if userInput == 'north':
            if express.direction == 'south':
                express.switch('north')
        if userInput == 'south':
            if express.direction == 'north':
                express.switch('south')
