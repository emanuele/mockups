from multiprocessing import Process, Queue
from time import time, sleep
import sys, os

def child(q, inp, t0):
    delta_t = time() - t0
    print("Child process started in %ssec." % delta_t)
    a = inp.readline()
    delta_t = time() - t0
    print("Child: key pressed after %ssec." % delta_t)
    print("Child: sending delta_t=%s." % delta_t)
    q.put(delta_t)
    print("Child: sent.")


if __name__ == '__main__':
    inp = os.fdopen(os.dup(sys.stdin.fileno())) # Maybe this does not work on win32

    for i in range(10):
        print("Parent: iteration %d" % i)
        print("Parent: Creating Queue and child Process.")
        q = Queue()
        t0 = time()
        p = Process(target=child, args=(q, inp, t0))
        print("Parent: Starting Child process.")
        p.start()
        print("Parent: waiting some seconds.")
        sleep(4)
        print("Parent: retriving data from child process.")
        if not q.empty:
            t_child = q.get(block=False)
        else:
            print("Parent: Child did not press a key.")

        print("Parent: terminating child process.")
        p.terminate()
        print("")
        print("")

