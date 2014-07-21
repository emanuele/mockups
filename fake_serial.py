from time import sleep
from random import random, choice, seed


class Serial(object):
    def __init__(self, values, start=[], timeout=2.0, seed=0, verbose=False, *args, **kwargs):
        self.values = values
        self.timeout = timeout
        seed = 0
        self.verbose = verbose
        self.start = start
        self.counter = 0

    def read(self, n_bytes):
        assert(n_bytes==1)
        if self.timeout < 0.0:
            return ''

        self.counter += 1
        if self.counter < len(self.start):
            if verbose: print("Serial: popping starting triggers.")
            return self.start[counter]

        if self.verbose: print("Serial: timeout = %s" % self.timeout)
        sleep(random() * self.timeout)
        return choice(self.values)

    def open(self):
        return 0

    def flushInput(self):
        return
