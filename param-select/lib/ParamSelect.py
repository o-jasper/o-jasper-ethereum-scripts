
class _Param():

    @property
    def text(self):
        return "Parameter for " + str(type(self))

    def parse(self, string):  # Parses a value.
        if len(string) == 0 or string == '\n':
            return self.default
        else:
            return self._parse(string)

    def choose_parse(self, string):
        return self.choose(self.parse(string))

    def okey(self, value):  # Returns if the value is okey.
        return true
    
   # Classifies values.(In context of tx firewall,
   # currently think maybe(might use different approach than returning numbers..)
   # *   0:    pass through, human oversight not necessary.
   # *   1:    ok, but human should look at it.
   # *   2:    human should really look at it and make decision.
   # * >=1024: bug/trust issue.
    def classify(self, value):
        return 0 if self.okey(value) else 1024


class Param(_Param):

    def __init__(self, name, default=None):
        self.name = name
        self.default = default

    def _parse(self,string):
        return eval(string)  # TODO too trustful.

    def choose(self, value):
        return (-1, value)

    #  Returns chosen value and next index list, given a value and index list..
    def i_choose(self, i, value=None):
        assert type(i) is list # and len(i) == 1

        j,ret = self.choose(value) #Index ignored, no index capability.
        return (i[:-1], ret)

    def tell(self):  # Return string describing self.
        return self.text + ("" if (self.default is None)
                                else " (default: " + str(self.default) + ")")

    def get(self, i):
        assert type(i) is list
#        assert len(i) == 1
        return self

class ParamBranch(_Param):

    def __init__(self, top, list=[]):
        self.top = top  # Top chooses from the list.
        self.list = list

    @property
    def name(self):
        return self.top.name

    def i_choose(self, i, value=None):
        assert type(i) is list

        if len(i) > 0:  # Already going down a path.
            return self.list[i[0]].i_choose(i[1:], value)
        else:  # First touch of branching, figure out the path.
            j,ret = self.top.choose(value)
            assert j >= 0
            return (i + [j], ret)

    def okey(self, value):
        return self.top.okey(value)

    def classify(self, value):
        return self.top.classify(value)

    def tell(self):
        return self.top.tell()

    def get(self, i):
        assert type(i) is list
        if len(i) == 0:
            return self
        elif i[0] < len(self.list):
            return self.list[i[0]].get(i[1:])
        else:
            return None

class ParamSequence(_Param):
    def __init__(self, list):
        self.list = list

    def i_choose(self,i , value=None):
        k = i[0]
        assert k < len(self.list)
        j,ret = self.list[k].i_choose(i[1:], value)
        if len(j) == 0:  # That path ran out, next one.
            return [k+1], ret
        else:  # Keep going on path.
            return i + j, ret

# Other parameters kinds in ParamKinds.py

class ParamSelect(ParamSequence):
    """Chain of choices, entries can choose between different branches.

    It can also act as a classifier of choices."""
    at_i = [0]

    def __init__(self, list, values={}):
        self.list    = list
        self.values  = values

    def get(self, i):
        assert type(i) is list and type(self.list) is list
        if len(i) == 0:
            return None
        elif i[0] < len(self.list):
            return self.list[i[0]].get(i[1:])
        else:
            return None

    @property
    def cur(self):
        return self.get(self.at_i)

    def choose(self, value=None):  # Choose and get the next.
        j,ret = self.i_choose(self.at_i, value)

        cur_class = self.cur.classify(value)  # Keep track of the worst class.
        to = (self.at_i, value, cur_class)  
        self.values[self.cur.name] = to # Set the value.

        self.at_i = j
        return to

    def update(self, i, value):
        if self.at_i[:len(i)] is i: #On active path, might change it.
            self.at_i = i
            ret = self.choose(value)
            while self.cur.name in self.values: #Move forward insofar it is set.
                self.choose(self.values[self.cur.name])
            return ret
        else:
            got = get(i)
            got.choose(value)  # (Might not do anything), but..)
            to = (i, value, got.classify(value))
            self.values[got.name] = to
            return to

    def choose_parse(self, string):
        return self.choose(self.cur.parse(string))

    def choose_list(self, values=[]):
        for v in values:
            self.choose(v)

    def tell(self):
        return self.cur.tell()

    # TODO reading settings.
    
    def list_names(self, names):
        list = []
        for el in names:
            list.append(self.values[el][1])
        return list
