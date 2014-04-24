
from ParamSelect import ParamSelect, ParamSequence
from ParamKindsGtk import figure_gui_el_vbox
from gi.repository import Gtk

class ParamSelectGtk(ParamSelect):

    def __init__(self, list, values={}, vbox=Gtk.VBox(False,0)):
        self.list    = list
        self.values  = values
        self.at_i = [0]

        self.gtk_el = figure_gui_el_vbox(list, ([],self), vbox=vbox)

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
            assert type(el) is ParamSequence
            for j in range(len(el.list)):
                el.show(i == j)  # Only show the one active.
        
