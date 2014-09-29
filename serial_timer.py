"""This is the serial_timer module which provides a low-level function
for measuring timings of triggers coming from the serial port. A
convenience class is available as well to mask low-level details to
the user.

Copyright (c) 2014, Emanuele Olivetti
Distributed under the BSD 3-clause license.
"""

from Queue import Queue
from threading import Thread


def serial_timer(q_in, q_out, t0, ser, time, good=['1','2'], bad=['5'], total_time=2000.0, verbose=False):
    delta_t = time() - t0
    if verbose: print("Child: started after %sms" % delta_t)
    while True:
        t0 = q_in.get(block=True, timeout=None)
        if t0 == 'stop':
            break

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
                q_out.put((inp, t), block=True, timeout=None)
                break
            elif inp == '':
                t = time() - t0
                if verbose: print("Child timeout: nothing arrived from serial after %s" % t)
                q_out.put(('timeout', t), block=True, timeout=None)
                break
            else:
                print("Child: Something wrong happened.")
                raise Exception
    
    print("Child: child thread terminating.")


class SerialTimer(object):
    """This class provides a timer for the serial port.
    """

    def __init__(self, t0, ser, time, good=['1','2'], bad=['5'], total_time=2000.0, flush=True, verbose=False):
        self.t0 = t0
        self.ser = ser
        self.time = time
        self.good = good
        self.bad = bad
        self.total_time = total_time
        self.flush = flush
        self.verbose = verbose

        self.q_in = Queue()
        self.q_out = Queue()
        self.t = Thread(target=serial_timer, args=(self.q_in, self.q_out, self.t0, self.ser, self.time, self.good, self.bad, self.total_time, self.verbose))
        self.t.daemon = True
        if self.verbose: print("SerialTimer: Starting child thread.")
        self.t.start()


    def start_timer(self, start_time=None):
        """Start measuring elapsed time.
        """
        if not self.t.is_alive():
            print("ERROR: Thread is not running!")
            raise Exception

        if start_time is None:
            start_time = self.time()

        self.start_time = start_time
        self.q_in.put(self.start_time)
        if self.verbose: print("SerialTimer: timer started.")
        return self.start_time


    def get_timing(self):
        """Get measured timing, if available.
        """
        if not self.t.is_alive():
            print("ERROR: Thread is not running!")
            raise Exception

        if self.verbose: print("SerialTimer: retriving data from child thread.")
        if not self.q_out.empty():
            inp, t_child = self.q_out.get(block=False)
            if self.verbose: print("SerialTimer: child returned %s and %s" % (inp, t_child))
        else:
            inp = None
            t_child = self.total_time
            if self.verbose: print("SerialTimer: child did not return values.")

        if self.flush: self.ser.flushInput()
        return inp, t_child


    def stop(self):
        """Stop child process.
        """
        if self.verbose: print("SerialTimer: stopping child process.")
        self.q_in.put('stop')
        self.t.join()
