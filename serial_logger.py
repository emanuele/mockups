"""Serial logger with timings.
"""

def serial_logger(q, t0, ser, time, good=[1,2], bad=[5], total_time=2000.0, verbose=False, close_queue=True):
    """Serial logger with timings.

    q: multiprocessing.Queue to communicate with parent process
    t0: time when child process was created
    ser : the Serial object, already opened
    good: trigger codes that we want to return to parent process
    bad: trigger codes that we want to discard
    time : timer function, in milliseconds
    total_time : in milliseconds
    """

    timeout = total_time

    while True:
        ser.timeout = timeout / 1000.0 # serial port wants seconds
        inp = ser.read(1)
        if verbose: print("Child: serial read %s" % inp)
        if inp in bad:
            timeout = (total_time - (time() - t0))
            continue
        elif inp in good:
            t = time() - t0
            if verbose: print("Child: %s arrived from serial after %s" % (inp, t))
            q.put((inp, t), block=True, timeout=None)
            break
        elif inp == '':
            t = time() - t0
            print("Child timeout: nothing arrived from serial after %s" % t)
            q.put(('timeout', t), block=True, timeout=None)
            break
        else:
            print("Child: Something wrong happened.")
            raise Exception

    if close_queue: q.close()
    
