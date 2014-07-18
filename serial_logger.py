"""Serial logger with timings.
"""

def serial_logger(q, t0, ser, good=[1,2], bad=[5], time, total_time=1000.0):
    """Serial logger with timings.

    q: multiprocessing.Queue to communicate with parent process
    t0: time when child process was created
    ser : the Serial object, already opened
    good: trigger codes that we want to return to parent process
    bad: trigger codes that we want to discard
    time : timer function, in milliseconds
    total_time : in milliseconds
    """

    timeout = total_time / 1000.0

    while True:
        ser.timeout = timeout
        inp = ser.read(1)
        if inp in bad:
            timeout = (total_time - (time() - t0)) / 1000.0 # in sec.
            continue
        elif inp in good:
            t = time()
            print("Child: %s arrived from serial after %s" % (inp, t))
            q.put((inp, t), block=True, timeout=None)
            break
        elif inp == '':
            t = time()
            print("Child timeout: nothing arrived from serial after %s" % t)
            q.put(('timeout', t), block=True, timeout=None)
            break
        else:
            # Something wrong happened.
            raise Exception

    q.close()
    
