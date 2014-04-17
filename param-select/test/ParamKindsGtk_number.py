#!/usr/bin/python
from gi.repository import Gtk

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)  # Stop program if closed.

import sys, os
from random import random, randrange

py_path = os.path.join(os.path.dirname(__file__), '../lib')
sys.path.append(py_path)

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
