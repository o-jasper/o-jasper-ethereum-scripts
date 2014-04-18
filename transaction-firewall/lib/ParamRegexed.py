import re
from ParamSelect import Param

class ParamRegexed(Param):
    def __init__(self, name, default, regex = ".*",
                 compiled=None, regex_anyway=None, classify_list=[]):
        self.name = name
        self.default = default
        if compiled is None:
            self.regex = regex
            self.compiled = re.compile(regex)
        else:
            self.regex = regex_anyway
            self.compiled = compiled
        self.classify_list= classify_list

    def okey(self, value):
        return type(value) is str and not self.compiled.match(value) is None

    def _parse(self, string):  # Could derive from ParamString but not worth it.
        return string

    def seek_correct(self, value, mode='strip'):
        if not type(value) is str:
            return None
        elif mode is 'strip':
            return value.strip()
        elif mode is 'single_white':  # Single whitespace only.
            list = value.split()
            ret = list[0]
            for el in list[1:]:
                ret += ' ' + el
            return ret
        else:
            return value

    def other_classify(self, value):
        for i in range(len(self.classify_list)):
            if not self.classify_list[i].match(value) is None:
                return i + 1
        return 0
