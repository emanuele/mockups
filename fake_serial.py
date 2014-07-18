from time import sleep
from random import random, choice, seed

class MySerial(object):
    def __init__(self, values, timeout=2.0, seed=0, verbose=False):
        self.values = values
        self.timeout = 2.0
        seed = 0
        self.verbose = verbose

    def read(self, n_bytes):
        assert(n_bytes==1)
        if self.verbose: print("MySerial: timeout = %s" % self.timeout)
        sleep(random() * self.timeout)
        return choice(self.values)

    def open(self):
        return 0
