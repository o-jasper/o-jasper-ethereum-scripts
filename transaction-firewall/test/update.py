from random import randrange, random
import choose

class TestExample(choose.TestBranch):

    # NOTE very limited, should check if at_i is changed correctly.
    def test_update(self):
        i,r = self.gi(), random()
        self.ps.update(i, r)
        val = self.ps.values[str(i[1:])]
        assert val[0] is i
        assert val[1] == r

    def test(self, n=100):
        for ignored in range(n):
            self.test_update()

TestExample().test()
