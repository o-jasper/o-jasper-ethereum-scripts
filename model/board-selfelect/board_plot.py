from board_math import *

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy

import math

def force_set_array(array, i, j, to):
    while len(array) <= j:
        array.append([])
    row = array[j]
    while len(row) <= i:
        row.append(0.0)
    row[i] = to

def make_rectangular_array(array):
    mw, maximum = 0, 0
    for row in array:
        for el in row:
            maximum = max(maximum, el)
        mw = max(len(row), mw)

    for i in range(len(array)):
        array[i] = map(lambda(x):x/maximum, array[i])
        while len(array[i]) < mw:
            array[i].append(0.0)
    return array, maximum, mw, len(array)

import random

def figure_array(field):
    array = []
    for k in field:
        g,b = k
        force_set_array(array, g,b, float(field[k].get("prob", 0)))
    return make_rectangular_array(array)

def fixed_array(field, w,h):
    array = map(lambda(x):map(lambda(y):0.0, range(w)), range(h))
    maximum = 0
    for k in field:
        g,b = k
        assert g>0 and b>=0
        if g < w and b < h:
            maximum = max(maximum, field[k].get("prob", 0.0))

    for k in field:
        g,b = k
        assert g>0 and b>=0
        if g < w and b < h:
            array[b][g] = field[k].get("prob", 0.0)/maximum
            

    return array, maximum, w,h

def plot(field):
    array, _, _, _ = figure_array(field)
    X = numpy.array(array)
    fig, ax = plt.subplots()
    ax.imshow(X, cmap=cm.jet, interpolation='none')

def plot_now(field):
    plot(field)
    plt.show()

def plot_vid(field, per_n=1, figure=True):
    array, max, w,h = fixed_array(field, 20, 10)
    p = plt.imshow(array, interpolation='none')
    fig = plt.gcf()
    i = 0
    while True:
        array, max, w,h = figure_array(field) if figure else fixed_array(field, 300, 180)
        p.set_data(array)
        flow_timestep(field, per_n)        
        plt.pause(0.5)
        i += 1
        print("*", i, w, h, max)
