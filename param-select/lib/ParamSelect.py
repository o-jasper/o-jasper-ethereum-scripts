
class _Param:

    @property
    def text(self):
        return "Parameter for " + str(type(self))

    def parse(self, string):  # Parses a value.
        if len(string) == 0 or string == '\n':
            return self.default
        else:
            return self._parse(string)

    def choose_parse(self, string):
        return self.i_choose(self.parse(string))

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
        assert type(i) is list and len(i) == 1

        j,ret = self.choose(value)
        return  ([i[0]+1], ret) if (j < 0) else (i+[j,0], ret)

    def tell(self):  # Return string describing self.
        return self.text + ("" if (self.default is None)
                                else " (default: " + str(self.default) + ")")

    def get(self, i):
        assert type(i) is list and len(i) == 0
        return self

class ParamList(_Param):

    def __init__(self, top, list=[]):
        self.top = top
        self.list = list

    def i_choose(self, i, value=None):
        assert type(i) is list and len(i) >= 1

        if len(i) == 1:
            return self.top.i_choose(i,value)
        else:
            j,ret = self.list[i[1]].i_choose(i[1:], value)
            return (i + j, ret)

    def okey(self, value):
        return self.top.okey(value)

    def classify(self, value):
        return self.top.classifiy(value)

    def tell(self):
        return self.top.tell()

    def get(self, i):
        assert type(i) is list
        if len(i) == 0:
            return self
        elif len(self.list) < i[0]:
            return self.list[i[0]].get(i[1:])
        else:
            return None

# Other parameters kinds in ParamKinds.py

class ParamSelect():
    """Chain of choices if one entry is a list.
    Things earlier in the list can select things later in the list.

    It can also act as a classifier of choices."""
    max_i = None
    max_class = 0

    at_i = [0]

    def __init__(self, list, values={}):
        self.list    = list
        self.values   = values

    def get(self, i):
        assert type(i) is list and len(i) >= 1
        if i[0] < len(self.list):
            return self.list[i[0]].get(i[1:])
        else:
            return None

    @property
    def cur(self):
        return self.get(self.at_i)

    def choose(self, value=None):
        ni,value = self.list[self.at_i[0]].i_choose(self.at_i, value)
        self.at_i = ni

        if self.cur is None:
            return None
        
      # Keep track of the worst class.
        cur_class = self.cur.classify(value)
        if self.max_class > cur_class or self.max_i is None:
            self.max_class = cur_class
            self.max_i = ni
        
        self.values[self.cur.name] = (value, cur_class) #  Set the value.
        return (ni, value)

    def choose_parse(self, string):
        return self.choose(self.cur.parse(string))

    def choose_list(self, values=[]):
        for v in values:
            self.choose(v)

    def tell(self):
        return self.cur.tell()

    def list(self, names):
        list = []
        for el in names:
            list.append(self.values[el][0])
        return list
