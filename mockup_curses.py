from multiprocessing import Process, Queue
from time import time, sleep
from test_curses import getch

def child(q, t0):
    delta_t = time() - t0
    print("Child process started in %ssec." % delta_t)
    key = getch("Please press a key")
    delta_t = time() - t0
    print("Child: %s key pressed after %ssec." % (key, delta_t))
    print("Child: sending delta_t=%s." % delta_t)
    q.put(delta_t)
    print("Child: sent.")


if __name__ == '__main__':

    for i in range(6):
        print("Parent: iteration %d" % i)
        print("Parent: Creating Queue and child Process.")
        t0 = time()
        q = Queue()
        p = Process(target=child, args=(q, t0))
        print("Parent: Starting Child process.")
        p.start()
        print("Parent: waiting some seconds.")
        sleep(5)
        print("Parent: retriving data from child process.")
        try:
            t_child = q.get(block=False)
            print("Parent: child pressed key in %ssec." % t_child)
        except:
            print("Parent: Child did not press a key.")
        print("Parent: terminating child process.")
        p.terminate()
        print("")
        print("")

