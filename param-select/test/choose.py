import sys, os
from random import random, randrange

py_path = os.path.join(os.path.dirname(__file__), '../lib')
sys.path.append(py_path)

from ParamSelect import ParamSelect, ParamBranch
from ParamKinds import ParamNumber

class TestBase:
    ps = None
    debug=False

    def num(self, name, opts=None):
        return ParamNumber(name=name, type=int, opts=opts)
    
    def list_pick(self, in_list):
        arr = []
        for el in in_list:
            if type(el) is int:
                arr.append(self.num(el))
            elif type(el) is list:
                arr.append(ParamBranch(self.num(el[0], opts=1), self.list_pick(el[1:])))
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

class TestPlain(TestBase):
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

for k in range(100):
    TestPlain().test()

class TestLinear(TestBase):
    def __init__(self, n=100, debug=False):
        self.debug = debug
        self.n = n
        self.pick(range(n))

    def test(self):
        for i in range(self.n):
            self.choose_assert(i, random())

TestLinear().test()
        
# Creates a param selector... I _just_ wanted a local function..
#class TestInstanceCreator:
#    def create_ps_list(self, N, p):
#        list = [sep()]
#        i = 0
#        while i < N:
#            arr = []
#            while random() < p:
#                arr.append(self.create_ps_list(N-i-1, p))
#            list.append(sep())
#            list.append(ParamBranch(sep(), arr) if len(arr)>0 else sep())
#            i += 1
#        return list
#
#    def create_ps(self, N, p):
#         return ParamSelect(self.create_ps_list(N, p))
#
#def some_val():
#    randrange(0, 100)
#
#def assert_str(a, b, str):
#    if not a is b:
#        print("%s: %s vs %s" % (str, a, b))
#        assert False
#
#def test_step(ps):
#    return not ps.choose(some_val()) is None
#
#j = 0
#while j < 10:
#    ps = TestInstanceCreator().create_ps(10, 0.35)
#    print(ps.cur) #TODO None??? WTF? The above setting shouldnt have any state?
#    i = 0
#    while test_step(ps):
#        i += 1
#        print("*" + str(i))
#    j += 1
#    print("--" + str(j))
#
