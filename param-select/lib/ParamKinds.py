from ParamSelect import Param

class ParamBasic(Param):

    def __init__(self, name, type, default=None):
        self.name = name
        self.type = type
        self.default = default

    @property
    def text(self):
        return "Basic parameter of type " + str(self.type)

    def okey(self, value):
        return type(value) is self.type

class ParamNumber(Param):

    def __init__(self, name, default=0):
        self.name       = name
        self.default    = default

    @property
    def text(self):
        return "Number-parameter"

    def okey(self, value):
        return type(value) is float or type(value) is int

    def _parse(self, string):
        return float(string)

class ParamNumberSep(ParamNumber):  # Single value, multiple cases.
    def __init__(self, name, threshhold=0, default=0):
        self.name       = name
        self.default    = default
        self.threshhold = threshhold

    def choose(self, value=None):
        if value is None:
            value = self.default
        return (0 if (value < self.threshhold) else 1, value)

class ParamInt(Param):

    def __init__(self, name, default=0):
        self.name       = name
        self.default    = default
        assert self.okey(self.default)

    @property
    def text(self):
        return "Integer-parameter"

    def okey(self, value):
        return type(value) is int

    def _parse(self, string):
        return int(string)

class ParamIntSep(ParamInt):

    def __init__(self, name, default=0, max=None):
        self.name    = name
        self.default = default
        self.max     = max

    def choose(self, value=None):
        if value is None:
            ret = (0 if (self.default is None) else self.default)
            return (ret, ret)
        return ((value if self.max is None else max(value, self.max)),value)

class ParamNumberListRanges(Param):
    """List of ranges parameter. Also has a minimum and maximum.
    """
    def __init__(self, name, default=0, type=None, min=None,max=None,opts=[]):
        self.name    = name
        self.default = default
        self.type    = type
        self.min     = min
        self.max     = max
        self.opts    = opts  # Rising list of numbers < all index 0  otherwise more.

    def okey(self, value):
        tp = type(value)
        if self.type is None:
            if not (tp is int or tp is float):
                return False
        elif self.type == tp:
            return False
        # Either wrong type or out of the range
        if not self.min is None and value < self.min:
            return False
        if not self.max is None and value > self.max:
            return False
        return True

    def _parse(self, string):
        return int(string) if (self.type == int) else float(string)

    def choose(self, value=None):
        if value is None:
            value = self.default

        for i in range(len(self.opts)):
            if self.opts[i] > value:
                return (i, value)

        return (len(self.opts), value)

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
        return ((-1, value) if (i is None) else (i,list[i]))

    def tell(self):
        text = ("options:" if (self.text == "") else self.text)
        ret = (text + ("" if (self.default is None) else "(" + self.default + ")"))
        for el in self.list:
            ret += el
        return ret

class WrongResult(Param):

    def okey(self, value):
        return False
