#!/usr/bin/python

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib/gui'))

from gi.repository import Gtk

from ParamSelectGtk import *
from ParamKinds import *
from ParamSelect import ParamBranch

ps = ParamSelectGtk([ParamNumber("float"), ParamBasic("first",str),
                     ParamListBox("list",["a","b"]),
                     [ParamInt("int", opts=1),
                      ParamBasic("string",str),
                      ParamNumber("num",str)]])
                    

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)  # Stop program if closed.

win.add(ps.gtk_el)

win.show_all()
Gtk.main()
