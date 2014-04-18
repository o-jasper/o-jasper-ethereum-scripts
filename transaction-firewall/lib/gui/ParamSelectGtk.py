
from ParamSelect import ParamSelect
from ParamKindsGtk import *
from gi.repository import Gtk

def element_associate_gtk(of, i, parent):
    if of.gtk is not None:
        return of.gtk
    elif type(of) is ParamList:
        of.gtk = ParamListGtk(top=associate_gtk_element(of.top,i, parent),
                              parentinfo=(i,parent))
    elif type(of) is ParamNumber:
        of.gtk = ParamNumberGtk(min=w.min, max=self, parentinfo=(i,parent))

    if len(i) >= 2
        parent.get(i[-2]).gtk_add(of.gtk)

    return of.gtk

def list_associate_gtk(list, vbox, i, parent):
    j = 0
    for el in list:
        vbox.pack_end(element_associate_gtk(el, i + [j], parent))
        j += 1
    return vbox

class ParamSelectGtk(ParamSelect):

    collapse_seq = []  # Sequence that would collapse when undoing.
    vbox = None

    def __init__(self, list, values={} vbox=Gtk.VBox(False,0)):
        self.list    = list
        self.values  = values

        self.vbox = list_associate_gtk(list, vbox)
        return self.vbox

    def choose(self, value):
        before_i = self.at_i
        ni,value = super(self,ParamSelectGtk).choose(value)

     #Deepened, activate ni that option.(de-activating others)
        if len(ni) > len(before_i): 
            self.get(ni[:-1]).active_option(ni[-1])

        return ni, value

    def update_show(self):
        for el in self.list:
            el.gtk.show()

        el = self
        for i in self.at_i[-1:]:
            el = el.list[i]
            assert type(el) is ParamList
            for j in range(len(el.list)):
                el.show(i == j)  # Only show the one active.
        
