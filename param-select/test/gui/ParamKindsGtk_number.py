#!/usr/bin/python
#
# Tests some gui elements for parameter selection alone.

from gi.repository import Gtk

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)  # Stop program if closed.

import sys, os
from random import random, randrange

def add_path(str):
    sys.path.append(os.path.join(os.path.dirname(__file__), str))

add_path('../../lib')
add_path('../../lib/gui')

import ParamKindsGtk
from ParamKindsGtk import ParamNumberGtk, ParamStringGtk
from ParamKinds import ParamNumber, ParamBasic

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)  # Stop program if closed.

p = ParamNumberGtk(ParamNumber('mew'))
s = ParamStringGtk(ParamBasic('miauw',str))

win.add(ParamKindsGtk.pack_end([p.gtk_el, s.gtk_el]))

win.show_all()
Gtk.main()
