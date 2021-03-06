from Queue import Queue
from threading import Thread
import time
from serial_logger import serial_logger
from fake_serial import Serial
from time import sleep
import sys


def mytime():
    return time.time() * 1000.0

if __name__ == '__main__':

    # f = open('log.txt', 'w')
    # sys.stdout = f

    ser = Serial(values=[1,2,5,5,5,5,5,5,5,5], timeout=2.0, seed=1, verbose=True)
    ser.open()

    for i in range(10):
        print("Parent: iteration %d" % i)
        print("Parent: Creating Queue and child Thread.")
        q = Queue()
        t0 = mytime()
        t = Thread(target=serial_logger, args=(q, t0, ser, mytime, [1,2], [5], 1000.0, True, False))
        t.daemon = True
        print("Parent: Starting Child thread.")
        t.start()
        print("Parent: waiting some seconds.")
        sleep(4)
        print("Parent: retriving data from child thread.")
        if not q.empty():
            inp, t_child = q.get(block=False)
            print("Parent: Child returned %s and %s" % (inp, t_child))
        else:
            print("Parent: Child did return values.")

        if t.is_alive():
            print("Parent: unexpectedly child thread is alive.")
            raise Exception

        print("Parent: child thread terminated.")
        print("")
        print("")
    
    
