#!/usr/bin/python

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib/gui'))

from gi.repository import Gtk

from ParamSelectGtk import *
from ParamKinds import *

ps = ParamSelectGtk([ParamNumber("float"), ParamInt("int"),
                    ParamBasic("string",str)], {'a':'b'})

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)  # Stop program if closed.

win.add(ps.gtk_el)

win.show_all()
Gtk.main()
