from time import sleep
from random import random, choice, seed
import sys

class Serial(object):
    def __init__(self, values, start=[], timeout=2.0, seed=0, verbose=False, output=None, *args, **kwargs):
        self.values = values
        self.timeout = 2.0
        seed = 0
        self.verbose = verbose
        self.start = start
        self.counter = 0
        if output is not None:
            sys.stdout = output

    def read(self, n_bytes):
        assert(n_bytes==1)
        if self.timeout < 0.0:
            return ''

        self.counter += 1
        if self.counter < len(self.start):
            if verbose: print("Serial: popping starting triggers.")
            return self.start[counter]

        if self.verbose: print("MySerial: timeout = %s" % self.timeout)
        sleep(random() * self.timeout)
        return choice(self.values)

    def open(self):
        return 0

    def flushInput(self):
        return
