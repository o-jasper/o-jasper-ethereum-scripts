#!/usr/bin/env python

import sys, os
from types import *

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from ParamSelect import *
from ParamKinds import *

ps = ParamSelect([ParamNumber("float"), ParamInt("int"),
                  ParamBasic("string",str)], {'a':'b'})

print("Specify")
ps.tell()
for line in sys.stdin:
    ps.choose_parse(line)
    if ps.cur is None:
        break
    ps.tell()

print("Done")
print(str(ps.values))
print("")
print(str(ps.list_names(['float','int','string'])))
