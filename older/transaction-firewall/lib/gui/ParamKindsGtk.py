# from ParamKinds import *
from gi.repository import Gtk
from ParamKinds import *
from ParamSelect import ParamSequence, ParamBranch

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

class ParamGtkBase:
    hidden = True

    def __init__(self, it, parentinfo=None):
        self.it = it
        self.parentinfo = parentinfo

    def value_changed(self, value):
        if not self.parentinfo is None:
            i,parent = self.parentinfo
            parent.update(i, self.get_value())

    def hide(self):
        if not self.hidden:
            self.gtk_el.hide()
            self.hidden = True

    def show(self, show=True):
        if not show:
            self.hide()                                 
        elif self.hidden:
            self.gtk_el.show()
            self.hidden = False

class ParamSequenceGtk(ParamGtkBase):
    """Just for ParamSequence"""
    def __init__(self, top=None, parentinfo=None, max=None):
        self.top = top
        self.gtk_el = vbox([top])
        # self.parentinfo = parentinfo
    def gtk_set(self, value):
        self.top.gtk_set(value)  # It does the parent stuff.

    def gtk_add(self, added):
        self.gtk_el.pack_end(added, True, True, 0)

class ParamNumberGtk(ParamGtkBase):
    """For next to any number param kind"""
    def __init__(self, it, parentinfo=None, digits=None, size=600, climb_rate=None):
        self.parentinfo = parentinfo
        self.it = it
        
        fx,tx = if_none(0, it.min),if_none(1, it.max)
        climb_rate = if_none((tx - fx)/100.0, climb_rate)

        if it.type is int:
            assert digits is None
            digits = 0
            fx,tx = if_none(0, it.min),if_none(100, it.max)
            climb_rate = 1
        
        self.adjustment = Gtk.Adjustment(value=if_none(fx, it.default), lower=fx, upper=tx,
                                         step_incr=climb_rate, page_incr=5*climb_rate)

        self.spinner = Gtk.SpinButton(adjustment=self.adjustment,
                                      climb_rate=climb_rate, digits=if_none(2,digits))
        self.spinner.set_range(fx, tx)
        self.spinner.name = it.name

        self.hscrollbar = Gtk.HScrollbar(self.adjustment)
        self.hscrollbar.set_min_slider_size(size)

        self.adjustment.connect('value-changed', self.adjustment_value_changed)
#        self.spinner.connect('change-value', self.spinner_change_value)

        self.gtk_el = pack_start([Gtk.Label(it.name + ":"), self.spinner,self.hscrollbar])

    def adjustment_value_changed(self, adjustment):
        self.value_changed(adjustment.get_value())
        return 0
            
    def spinner_change_value(self, sb, st):
        print('---',st)
        print(Gtk.GTK_SCROLL_STEP_UP)
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
        if self.it.type is int:
            return int(self.adjustment.get_value())
        else:
            return self.adjustment.get_value()

class ParamStringGtk(ParamGtkBase):
    def __init__(self, it, parentinfo=None):
        self.parentinfo = parentinfo

        self.entry = Gtk.Entry()
    
        self.entry.connect("changed", self.entry_changed)
        
        self.gtk_el = pack_start([Gtk.Label(it.name + ":"), self.entry])

    def entry_changed(self, entry):
        self.value_changed(entry.get_text())

    def set_value(self, value):
        self.entry.set_text(value)
    def get_value(self):
        return self.entry.get_text()

class ParamListBoxGtk(ParamGtkBase):
    def __init__(self, it, parentinfo=None):
        self.parentinfo = parentinfo

        self.combo = Gtk.ComboBoxText()
        for el in it.list:
            self.combo.append_text(str(el))
        self.combo.connect("changed", self.combo_changed)

        self.gtk_el = pack_start([Gtk.Label(it.name + ":"), self.combo])

    def combo_changed(self, combo):
        self.value_changed(combo.get_active())
    
    def set_value(self, value):
        for i in range(len(it.list)):
            if it.list[i] is value:
                self.entry.set_active(i)
    def get_value(self):
        return max(self.entry.get_active(), 0)
        

# Figures out which gui element fits with the parameter kind, and adds it.
def figure_gui_el(of, parentinfo):
    if of.gtk is not None:
        return of.gtk

    elif type(of) is ParamSequence:
        of.gtk = ParamSequenceGtk(figure_gui_element(of.top,i, parent), parentinfo)

    elif type(of) is ParamNumber:
        of.gtk = ParamNumberGtk(of, parentinfo)

    elif type(of) is ParamString:
        of.gtk = ParamStringGtk(of,  parentinfo)

    elif type(of) is ParamBasic:
        if of.type is str:
            of.gtk = ParamStringGtk(of, parentinfo)
        elif of.type is int or of.type is number:
            of.gtk = ParamNumberGtk(of, parentinfo)

    elif type(of) is ParamListBox:
        of.gtk = ParamListBoxGtk(of, parentinfo)

    elif type(of) is ParamBranch:
        of.gtk = figure_gui_el(of.top, parentinfo)  # TODO

    i = parentinfo[0]
    if len(i) >= 2:
        parent.get(i[-2]).gtk_add(of.gtk)

    return of.gtk

def figure_gui_el_vbox(list, parentinfo, vbox=Gtk.VBox()):
    i, parent = parentinfo
    j = 0
    for el in list:
        got = figure_gui_el(el, (i + [j], parent))
        if got is not None:
            vbox.pack_end(got.gtk_el, True,True,0)
        else:
            print(got,el)
        j += 1
    return vbox
