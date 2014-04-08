
from iter_tree import IterTree

class Param:
    text = ""
    default = None

    def value_parse(self, string):
        return eval(string)  # TODO too trustful.

    def choose_parse(self, string):
        return self.choose(self.value_parse(string))

    def okey(self):  # Great naming..
        return true
    
   # Classify.(In context of tx firewall,
   # currently think maybe(might use different approach than returning numbers..)
   # *   0:    pass through, human oversight not necessary.
   # *   1:    ok, but human should look at it.
   # *   2:    human should really look at it and make decision.
   # * >=1024: invalid input/bug/trust issue.
    def classify(self, value):
        return 0 if self.okey() else 1024

    def tell(self):
        print(self.text + ("" if (self.default is None) else "(" + self.default + ")"))

class ParamBasic(Param):
    def __init__(self, name, type, default=None):
        self.name = name
        self.type = type
        self.default = default

    def okey(self, value):
        return type(value) is self.type

    def choose(self, value=None):
        return (value, 0)

class ParamListBox(Param):
    def __init__(self, name, list, default=None):
        self.name = name
        self.list = list
        self.default = default

    def find(value):
        for i in range(len(self.list)):
            if list[i] == value:
                return i
        return None

    def okey(self, value):
        return self.find(value) is None

    def choose(self, value=None):
        if value is None:
            value = self.default
        i = self.find(value)
        return (None if (i is None) else (list[i],i))

    def tell(self):
        text = ("options:" if (self.text == "") else self.text)
        print(text + ("" if (self.default is None) else "(" + self.default + ")"))
        for el in self.list:
            print(el)

class ParamIntSep(Param):
    def __init__(self, name, default=0):
        self.name    = name
        self.default = default

    def okey(self, value):
        return type(value) is int

    def choose(self, value=None):
        if value is None:
            return (self.default, self.default)
        return (value, value)

    def parse(self, string):
        return self.choose(int(string))

class ParamValueSep(Param):  # Single-value
    def __init__(self, name, threshhold=0, default=0):
        self.name       = name
        self.default    = default
        self.threshhold = threshhold

    def okey():
        return type(value) is float or type(value) is int

    def choose(self, value=None):
        if value is None:
            value = self.default
        return (value, 0 if (value < self.threshhold) else 1)

    def parse(self, string):
        return self.choose(float(string))

class ParamSelect(IterTree):
    """Chain of choices if one entry is a list.
    Things earlier in the list can select things later in the list.

    It can also act as a classifier of choices."""
    max_class = 0

    def __init__(self, chain, values={}):
        self.chain    = chain
        self.values   = values

    def choose(self, value=None):
        assert len(self.in_chain) > 0
        print(string(value) + " + " + string(type(value)))
        value, ni = self.cur.choose(value)
      # Keep track of the worst class.
        class = self.cur.classify(value)
        self.max_class = max(self.max_class, class)
        
        self.values[self.cur.name] = (class, value) #  Set the value.
        self.next(ni)

    def choose_parse(self, string):
        return self.choose_parse(string)

    def choose_list(self, values=[]):
        for v in values:
            self.choose(v)

    def tell(self):
        self.cur.tell()
