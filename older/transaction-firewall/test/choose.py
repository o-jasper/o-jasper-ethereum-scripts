import sys, os
from random import random, randrange

py_path = os.path.join(os.path.dirname(__file__), '../lib')
sys.path.append(py_path)

from ParamSelect import ParamSelect, ParamBranch
from ParamKinds import ParamNumber

class TestBase:
    def __init__(self):
        self.ps = None
        self.debug = False

    def num(self, name, opts=None):
        return ParamNumber(name=name, type=int, opts=opts)
    
    def list_pick(self, in_list):
        arr = []
        for el in in_list:
            if type(el) is list:
                arr.append(ParamBranch(self.num(el[0], opts=1), self.list_pick(el[1:])))
            else:
                arr.append(self.num(el))
        return arr

    def pick(self, list):
        self.ps = ParamSelect(self.list_pick(list))

    def choose_assert(self, name, v):
        if self.debug:
            print('at:', self.ps.at_i)
        assert not self.ps.cur is None
        self.ps.choose(v)
        if self.debug:
            print(self.ps.values, name, v)
        assert name in self.ps.values
        if self.debug:
            print('-', name, ": ", v, " vs ", self.ps.values[name])
        assert self.ps.values[name][1] == v

class TestExample(TestBase):
    def __init__(self, debug=False):
        self.debug = debug
        self.pick([1,2,[3,7,8,[4,5,6]],10])

    def test(self):
        if self.debug:
            print("*------------*")

        self.choose_assert(1, random())
        self.choose_assert(2, random())
        r = randrange(3)
        self.choose_assert(3, r)
        if r == 2:
            r2 = randrange(2)
            self.choose_assert(4, r2)
            self.choose_assert(5 + r2, 7.778)
        else:
            self.choose_assert(7 + r, random())
        self.choose_assert(10, random())
        assert self.ps.cur is None

for k in range(100):
    TestExample().test()

class TestLinear(TestBase):
    def __init__(self, n=100, debug=False):
        self.debug = debug
        self.n = n
        self.pick(range(n))

    def test(self):
        for i in range(self.n):
            assert not self.ps.cur is None
            self.choose_assert(i, random())
        assert self.ps.cur is None

TestLinear().test()

class TestBranch(TestBase):
    def __init__(self, n=3, depth=4, debug=False):
        self.debug = debug

        self.depth = depth
        self.n = n

        self.arr = [self.gen_arr(n, depth, [])]
        self.pick(self.arr)
        
    def gen_arr(self, n, depth, p):
        arr = []
        if depth < 0:
            return str(p)
        else:
            arr.append(str(p))
            for i in range(n):    
                arr.append(self.gen_arr(n, depth-1, p + [i]))
        return arr

    def gi(self, depth=None):
        if depth is None:
            depth = randrange(self.depth)
        assert depth < self.depth
        i = [0]
        for el in range(max(0,depth-1)):
            i.append(randrange(self.n))
        return i

    def test_get(self, n=100):
        for el in range(n):
            i = self.gi()
            assert self.ps.get(i) is not None

    def test_choose(self):
        if self.debug:
            print('got', self.arr)
            print('--')
        at = []
        for el in range(self.depth + 1):
            r = randrange(self.n)
            assert not self.ps.cur is None
            self.choose_assert(str(at), r)
            at.append(r)
            assert [0] + at == self.ps.at_i
        self.choose_assert(str(at), 5.55)
        assert self.ps.cur is None

    def test(self):
        self.test_get()
        self.test_choose()

TestBranch().test()
