from Queue import Queue
from threading import Thread
import time
from serial_timer import serial_timer
from fake_serial import Serial
from time import sleep
import sys


def mytime():
    return time.time() * 1000.0

if __name__ == '__main__':

    # f = open('log.txt', 'w')
    # sys.stdout = f

    ser = Serial(values=[5,5,5,5,5,5,5,5], timeout=2.0, seed=1, verbose=True)
    ser.open()

    print("Parent: Creating Queue and child Thread.")
    q_in = Queue()
    q_out = Queue()
    t0 = mytime()
    t = Thread(target=serial_timer, args=(q_in, q_out, t0, ser, mytime, [1,2], [5], 1000.0, True))
    t.daemon = True
    print("Parent: Starting Child thread.")
    t.start()

    for i in range(10):
        print("Parent: iteration %d" % i)
        q_in.put(mytime())
        print("Parent: waiting some seconds.")
        sleep(4)
        print("Parent: retriving data from child thread.")
        if not q_out.empty():
            inp, t_child = q_out.get(block=False)
            print("Parent: Child returned %s and %s" % (inp, t_child))
        else:
            print("Parent: Child did return values.")

        print("")
    
    q_in.put('stop')
    
