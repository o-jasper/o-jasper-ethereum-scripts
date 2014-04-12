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
        return (value, 0 if (value < self.threshhold) else 1)

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
        return (value, (value if self.max is None else max(value, self.max)))

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
