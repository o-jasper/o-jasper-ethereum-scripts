
from board_math import flow_timestep
from board_plot import plot

import pickle
import argparse

#parser = argparse.ArgumentParser(description="Models the thing.")

field = flow_timestep(100)
plot(field)
