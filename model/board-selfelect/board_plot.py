from board_math import *
import Gnuplot

#import matplotlib.pyplot as plt
#import matplotlib.cm as cm


def force_set_array(array, i, j, to):
    while len(array) <= j:
        array.append([])
    row = array[j]
    while len(row) <= i:
        row.append(0)
    row[i] = to

def plot(field):
    ret = []
    for k in field:
        g,b = k
        force_set_array(ret, g,b, field[k].get("prob", 0))

    g = Gnuplot.Gnuplot(debug=1)
    g("set pm3d map")
    g.plot(ret)
