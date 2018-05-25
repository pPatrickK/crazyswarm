#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

import sys

try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        # FIXME what to do on other platforms?
        # Just give up here.
        raise ImportError('getch not available')
    else:
        getch = msvcrt.getch
else:
    def getch():
        """getch() -> key character

        Read a single keypress from stdin and return the resulting character.
        Nothing is echoed to the console. This call will block if a keypress
        is not already available, but will not wait for Enter to be pressed.

        If the pressed key was a modifier key, nothing will be detected; if
        it were a special function key, it may return the first character of
        of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

Z = 0.5

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    #
    # # inp = input('Enter your input:')
    while True:
         result = getch()
        if result=='x':
            break
        elif result=='[B':
            print('pfeil unten')
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        #
        # elif result=='x':
        print(result)

    print('end of Programm')


    # allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
    # timeHelper.sleep(1.5+Z)
    # for cf in allcfs.crazyflies:
    #     pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
    #     cf.goTo(pos, 0, 1.0)
    #
    # print("press button to continue...")
    # swarm.input.waitUntilButtonPressed()
    #
    # allcfs.land(targetHeight=0.02, duration=1.0+Z)
    # timeHelper.sleep(1.0+Z)
