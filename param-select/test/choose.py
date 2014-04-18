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
            print(self.ps.at_i)
        assert not self.ps.cur is None
        self.ps.choose(v)
        if self.debug:
            print(self.ps.values, name, v)
        assert name in self.ps.values
        if self.debug:
            print(name, ": ", v, " vs ", self.ps.values[name])
        assert self.ps.values[name][1] == v

class TestExample(TestBase):
    def __init__(self, debug=False):
        self.debug = debug
        self.pick([1,2,[3,4,5,6],7])

    def test(self):
        self.choose_assert(1, random())
        self.choose_assert(2, random())
        r = randrange(3)
        self.choose_assert(3, r)
        self.choose_assert(4 + r, random())
        self.choose_assert(7, random())
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
    def __init__(self, n=2, depth=2, debug=False):
        self.debug = debug

        self.depth = depth
        self.n = n

        self.arr = self.gen_arr(n, depth, [])
        print(self.arr)
        self.pick(self.arr)
        
    def gen_arr(self, n, depth, p):
        arr = []
        if depth < 0:
            for i in range(n):
                arr.append(str(p + [i]))
        else:
            arr.append(str(p))
            for i in range(n):    
                arr.append(self.gen_arr(n, depth-1, p + [i]))
        return arr
    
    def test(self):
        at = []
        print(self.ps.values)
        self.choose_assert('[]', random())
        for i in range(self.depth):
            r = randrange(self.n)
            at.append(r)
            # self.choose_assert(str(at), r)  #Hrmm
            self.ps.choose(r)
            assert at == self.ps.at_i[1:]

TestBranch(debug=True).test()
