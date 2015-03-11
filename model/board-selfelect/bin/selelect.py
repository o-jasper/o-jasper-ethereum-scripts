
from board_math import flow_timestep
from board_plot import plot, plot_now, plot_vid

import pickle
import argparse

#parser = argparse.ArgumentParser(description="Models the thing.")

field = flow_timestep({(10,0):{"prob":1.0}}, 1)
#plot_now(field)

plot_vid(field)
