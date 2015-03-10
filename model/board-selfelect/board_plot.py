from board_math import *
import Gnuplot

def plot(field):
    ret = []
    for k in field:
        ret.append(field[k]["prob"])
    g = Gnuplot.Gnuplot(debug=1)
    g("set pm3d map")    
    g.splot(ret)

