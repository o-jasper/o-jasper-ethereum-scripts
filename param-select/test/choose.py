import sys, os
from random import random, randrange

py_path = os.path.join(os.path.dirname(__file__), '../lib')
sys.path.append(py_path)

from ParamSelect import ParamSelect, ParamList
from ParamKinds import ParamNumber

class TestBase:
    k = 0
    ps = None

    def num(self, opts=None):
        self.k += 1
        return ParamNumber(name=self.k, type=int, opts=opts)

    def down(self, n=0, arr=None):
        top = self.num(opts=1)
        if arr is None:
            arr = []
            for el in range(n):
                arr.append(self.num())
        return ParamList(top, arr)

    def choose_assert(self, name, v):
        assert not self.ps.cur is None
        self.ps.choose(v)
        print(self.ps.values, name, v)
        assert name in self.ps.values
        assert self.ps.values[name][1] == v

class TestPlain(TestBase):
    n = randrange(2,4)
    def __init__(self):
        print(self.n)
        self.ps = ParamSelect([self.num(),self.num(),self.down(self.n),self.num()])

    def test(self):
        self.choose_assert(1, random())
        self.choose_assert(2, random())
        r = randrange(self.n)
        self.choose_assert(3, r)
        self.choose_assert(4 + r, random())
#        self.choose_assert(6 + self.n, random())

TestPlain().test()
        
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
#            list.append(ParamList(sep(), arr) if len(arr)>0 else sep())
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
