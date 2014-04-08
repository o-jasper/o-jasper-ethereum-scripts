#!/usr/bin/env python

import sys, os
from random import randrange

py_path = os.path.join(os.path.dirname(__file__), '../lib')
sys.path.append(py_path)

from iter_tree import IterTree

class SpecificTestIt():
    """Tests specific input.
    """
    it = IterTree([1, 2, [[3, 4, 5], [6, 7, 8]], 9, 10])

    def choice_check(self, opts, n=None):
        if n is None:
            i = randrange(len(opts))
            return self.it.next_choice(i) == opts[i]
        else:
            return self.it.next_choice(randrange(n)) == opts
    def only(self, result, n=100):
        return self.it.next_choice(randrange(n)) == result

    def run(self):
        assert self.it.cur == 1 and self.only(2)

        i = randrange(2)
        assert self.it.next_choice(i) == [3,6][i]
        if i == 0:
            assert self.only(4) and self.only(5)
        else:
            assert self.only(7) and self.only(8)
        assert self.only(9) and self.only(10)

SpecificTestIt().run()
