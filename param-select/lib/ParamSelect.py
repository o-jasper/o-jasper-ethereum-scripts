
from iter_tree import IterTree

class Param:

    def __init__(self, name, default=None):
        self.name = name
        self.default = default

    @property
    def text(self):
        return "Parameter for " + str(type(self))

    def parse(self, string):
        if len(string) == 0 or string == '\n':
            return self.default
        else:
            return self._parse(string)

    def _parse(self,string):
        return eval(string)  # TODO too trustful.

    def choose_parse(self, string):
        return self.choose(self.value_parse(string))

    def choose(self, value=None):
        return (value, 0)

    def okey(self, value):  # Great naming..
        return true
    
   # Classify.(In context of tx firewall,
   # currently think maybe(might use different approach than returning numbers..)
   # *   0:    pass through, human oversight not necessary.
   # *   1:    ok, but human should look at it.
   # *   2:    human should really look at it and make decision.
   # * >=1024: bug/trust issue.
    def classify(self, value):
        return 0 if self.okey(value) else 1024

    def tell(self):
        print(self.text + ("" if (self.default is None)
                           else " (default: " + str(self.default) + ")"))

# Other parameters kinds in ParamKinds.py

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
        value, ni = self.cur.choose(value)
      # Keep track of the worst class.
        cur_class = self.cur.classify(value)
        self.max_class = max(self.max_class, cur_class)
        
        self.values[self.cur.name] = (value, cur_class) #  Set the value.
        self.next_choice(ni)

    def choose_parse(self, string):
        return self.choose(self.cur.parse(string))

    def choose_list(self, values=[]):
        for v in values:
            self.choose(v)

    def tell(self):
        self.cur.tell()

    def list(self, names):
        list = []
        for el in names:
            list.append(self.values[el][0])
        return list
