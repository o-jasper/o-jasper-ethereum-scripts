# from ParamKinds import *
from gi.repository import Gtk

def is_number(x):
    return type(x) is float or type(x) is int

def if_none(alt, x):
    return (alt if (x is None) else x)

def pack_start(list, into=None):
    into = if_none(Gtk.HBox(False, 0), into)
    for el in list:
        into.pack_start(el, True, True, 0)
    return into

def pack_end(list, into=None):
    into = if_none(Gtk.VBox(False, 0), into)
    for el in list:
        into.pack_end(el, True, True, 0)
    return into

class ParamListGtk:
    """Just for ParamList"""
    hidden = True
    
    def __init__(self, top=None, max=None, parentinfo=None):
        self.top = top
        self.vbox = vbox([top])
        # self.parentinfo = parentinfo
    def gtk_set(self, value):
        self.top.gtk_set(value)  # It does the parent stuff.

    def gtk_add(self, added):
        self.vbox.pack_end(added, True, True, 0)

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
    """For next to any number param kind"""
    hidden = True
    
    def __init__(self, it, parentinfo=None, digits=2, size=600, climb_rate=None):
        self.min = it.min
        self.max = it.max
        self.parentinfo = parentinfo

        fx,tx = if_none(0, self.min),if_none(0, self.max)

        climb_rate = if_none((tx - fx)/100.0, climb_rate)
        self.adjustment = Gtk.Adjustment(value=if_none(fx, it.default), lower=fx, upper=tx,
                                         step_incr=climb_rate, page_incr=5*climb_rate)
        
        self.spinner = Gtk.SpinButton(adjustment=self.adjustment,
                                      climb_rate=climb_rate, digits=digits)
        self.spinner.set_range(if_none(0, self.min), if_none(1, self.max))
        self.spinner.name = it.name

        self.hscrollbar = Gtk.HScrollbar(self.adjustment)
        self.hscrollbar.set_min_slider_size(size)

        self.adjustment.connect('value-changed', self.adjustment_value_changed)
        self.spinner.connect('change-value', self.spinner_change_value)

        self.hbox = pack_start([Gtk.Label(it.name + ":"), self.spinner,self.hscrollbar])

    @property
    def gtk_el(self):
        return self.hbox

    def hide(self):
        if not self.hidden:
            self.hbox.hide()
            self.hidden = True

    def show(self, show=True):
        if not show:
            self.hide()
        elif self.hidden:
            self.hbox.show()
            self.hidden = False
    
    def adjustment_value_changed(self, adjustment):
        self.value_changed(adjustment.get_value())
        return 0
            
    def value_changed(self, value):
        if not self.parentinfo is None:
            i,parent = self.parentinfo
            parent.update(i, value)

    def spinner_change_value(self, sb, st):
        print(st)
        adj = sb.get_adjustment() 
        val = adj.get_value()
        if st == Gtk.SCROLL_STEP_UP: #TODO cant figure names.. should be Gtk.SCROLL_STEP_UP
            adj.set_value(val + adj.get_step_increment())
        elif st == Gtk.SCROLL_STEP_DOWN:
            adj.set_value(val - adj.get_step_increment())
        elif st == Gtk.SCROLL_PAGE_UP:
            adj.set_value(val + adj.get_page_increment())
        elif st == Gtk.SCROLL_PAGE_DOWN:
            adj.set_value(val - adj.get_page_increment())
        elif st == Gtk.SCROLL_START:
            adj.set_value(adj.get_lower())
        elif st == Gtk.SCROLL_END:
            adj.set_value(adj.get_upper())
        return 0

    def set_value(self, value):
        self.adjustment.set_value(value)  # Should trigger value changed.

    def get_value(self):
        return self.adjustment.get_value()

class ParamStringGtk():

    hidden = True

    @property
    def gtk_el(self):
        return self.hbox

    
    def __init__(self, it, parentinfo=None):
        self.entry = Gtk.Entry()
        self.hbox = pack_start([Gtk.Label(it.name + ":"), self.entry])
