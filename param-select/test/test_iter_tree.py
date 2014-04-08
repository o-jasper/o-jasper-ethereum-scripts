#!/usr/bin/env python

import sys, os
from random import randrange

py_path = os.path.join(os.path.dirname(__file__), '../lib')
sys.path.append(py_path)

from iter_tree import IterTree

class SpecificTest():
    """Tests specific input."""
    it = IterTree([1, 2, [[3, 4, 5], [6, 7, 8]], 9, 10])

    def only(self, result, n=100):
        return self.it.next_choice(randrange(n)) == result

    def run(self):
        i = randrange(2)
        assert self.it.cur == 1 and self.only(2)
        assert self.it.next_choice(i) == [3,6][i]
        assert self.only([4,7][i]) and self.only([5,8][i])
        assert self.only(9) and self.only(10)
        assert self.only(None)

SpecificTest().run()
