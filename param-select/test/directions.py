import sys, os
from random import random, randrange

py_path = os.path.join(os.path.dirname(__file__), '../lib')
sys.path.append(py_path)

from ParamSelect import ParamSelect
from ParamKinds import ParamIntSep

# Creates a param selector... I _just_ wanted a local function..
class TestInstanceCreator:
    k = 0
    def sep(self):
        self.k += 1
        return ParamIntSep(name=self.k)

    def create_ps_list(self, N, p):
        list = [self.sep()]
        i = 0
        while i < N:
            arr = []
            while random() < p:
                arr.append(self.create_ps_list(N-i-1, p))
            list.append(self.sep())
            list.append(arr if len(arr)>0 else self.sep())
            i += 1
        return list

    def create_ps(self, N, p):
         return ParamSelect(self.create_ps_list(N, p))

def some_val():
    randrange(0, 100)

def assert_str(a, b, str):
    if not a is b:
        print("%s: %s vs %s" % (str, a, b))
        assert False

def test_step(ps):
    if (ps.cur is None):
        return False
    
    if len(ps.in_chain) <= 1:  #Dropping out.
        at = ps.at.copy()
        ps.choose(some_val())
        if len(at) <= 2:
            assert_str(ps.cur, None, "E DO None(<=2)")
        else:
            at = at[:-2]
            at[-1] += 1
            got = ps.get_at(at)
            if got is None:
                assert_str(ps.cur, None, "E DO None")
            else:
                assert_str(ps.cur, got[0], "E DO")
    elif ps.in_chain is list and type(ps.in_chain[1]) is list:  # Choosing on.
        i = randrange(len(ps.in_chain[1]))
        expect = ps.in_chain[1][i][0]
        ps.choose(i)
        assert_str(ps.cur, expect, "E C")
    else:  # Dropping out again?
        ps.choose(some_val())
    return not (ps.cur is None)

j = 0
while j < 10:
    ps = TestInstanceCreator().create_ps(10, 0.35)
    print(ps.cur) #TODO None??? WTF? The above setting shouldnt have any state?
    i = 0
    while test_step(ps):
        i += 1
        print("*" + str(i))
    j += 1
    print("--" + str(j))
