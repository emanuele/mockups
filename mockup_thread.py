from Queue import Queue
from threading import Thread
from time import time, sleep
import sys, os

def child(q, t0):
    # delta_t = time() - t0
    # print("Child thread started in %ssec." % delta_t)
    # a = raw_input()
    delta_t = time() - t0
    print("Child: key pressed after %ssec." % delta_t)
    q.put(delta_t)
    

if __name__ == '__main__':

    for i in range(10):
        print("Parent: iteration %d" % i)
        print("Parent: Creating child Thread.")
        q = Queue()
        t0 = time()
        t = Thread(target=child, args=(q, t0))
        t.daemon = True
        # print("Parent: Starting child thread.")
        t.start()
        # print("Parent: waiting some seconds.")
        sleep(1)

        if not q.empty():
            t_child = q.get()
            print("Parent: got this from child thread %ssec." % t_child)
        else:
            print("Parent: nothing arrived from child thread.")
                
        if t.is_alive():
            print("Parent: terminating child thread.")
            t.terminate()

        print("Parent: child thread terminated.")
        print("")
        print("")

