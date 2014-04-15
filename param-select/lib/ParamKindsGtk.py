# from ParamKinds import *
from gi.repository import Gtk

def is_number(x):
    return type(x) is float or type(x) is int

def if_none(alt, x):
    return (alt if (x is None) else x)

def hbox(list, hbox=HBox(False, 0)):
    for el in list:
        hbox.pack_end(el)

def vbox(list, hbox=VBox(False, 0)):
    for el in list:
        vbox.pack_end(el)

class ParamListGtk():

    hidden = True
    
    def __init__(self, top=None, max=None, parentinfo=None):
        self.top = top
        self.vbox = vbox([top])
        # self.parentinfo = parentinfo
    def gtk_set(self, value):
        self.top.gtk_set(value)  # It does the parent stuff.

    def gtk_add(self, added):
        self.vbox.pack_end(added)

    def hide(self):
        if not self.hidden:
            self.vbox.hide()
            self.hidden = True

    def show(self, show=True):
        if not show:
            if self.hidden:
                self.vbox.show()
                self.hidden = False
        else:
            self.hide()

class ParamNumberGtk():

    hidden = True
    
    def __init__(self, min=None, max=None, parentinfo=None):
        self.min = min
        self.max = max
        self.parentinfo = parentinfo

        self.entry = Gtk.Entry()
        self.spin  = Gtk.SpinButton()

        self.spin.connect('input', self.spinner_input)
        self.entry.connect('input', self.entry_input)
        
        self.spin.name = self.name
        self.spin.set_range(if_none(0, self.min), if_none(1, self.max))

        self.hbox = hbox([self.entry,self.spin])
        return self.hbox

    def hide(self):
        if not self.hidden:
            self.hbox.hide()
            self.hidden = True

    def show(self, show=True):
        if not show:
            hide()
        elif self.hidden:
            self.hbox.show()
            self.hidden = False

    def set_value(self, value):
        i,parent = self.parentinfo
        parent.update(i, value)

    def gtk_set(self, value):
        self.spin.set_value(value)
        self.entry.set_text(str(value))
        self.set_value(value)

    def spinner_input(self, value):
        self.entry.set_text(str(value))
        self.set_value(value)

    def text_input(self, text):
        value = float(text)
        self.spinner.set_value(value)
        self.set_value(value)
