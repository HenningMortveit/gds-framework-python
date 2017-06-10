import sys

# modify to your dir
sys.path += ['C:/Users/vgncssd/Desktop/git_recent/gds']

import subprocess
import operator
from graphviz import Digraph
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import to_agraph
import copy
import itertools
import pickle
import cPickle
import math
import statsmodels as sm
import statsmodels.robust
import numpy
from collections import Counter

# from /gds/
import biographs
import phase_space
import graphs
import functions
import state
import gds.gds
import algorithms
import equivalence
import util.enumeration

# created by Ryan
import visualization
import phase_space_analysis


def get_example_gds():
    n = 4
    pi = [1, 0, 3, 2]
    X = graphs.CircleGraph(n)
    X.add_edge(0, 2)

    f = n * [functions.biThreshold(1, 3)]
    # f = n * [functions.nor]
    stateObject = n * [state.State(0, 2)]

    doCircle = False
    gds1 = gds.gds.GDS(X, f, stateObject, doCircle)
    gds1.SetSequence(pi)
    ps = phase_space.PhaseSpace(gds1)

    return gds1, ps


def visualization_example():
    gds1, ps = get_example_gds()
    pi = [1, 0, 3, 2]
    # pi shifted once to the left
    print "hit ratio:", visualization.Output_PS_Figures(gds1, pi, 1)


def max_transient_length_example():
    gds1, ps = get_example_gds()
    LT = phase_space_analysis.GetMaxTransientLength(ps, gds1)
    print "('representative periodic state (size of n-cycle): max transient length to n-cycle)"
    print LT


def attractor_basin_count_example():
    gds1, ps = get_example_gds()
    print "('representative periodic state (size of n-cycle): total states connected to n-cycle)"
    print phase_space_analysis.GetCycleBasinCount(ps, gds1)


def GoE_count_example():
    gds1, ps = get_example_gds()
    print "('representative periodic state (size of n-cycle): GoE count in n-cycle)"
    print phase_space_analysis.GetGOECount(ps, gds1)


def activity_example():
    gds1, ps = get_example_gds()
    print "activity vector ('vertex': activity)"
    print phase_space_analysis.GetActivity(ps, gds1)


def LTActivity_example():
    gds1, ps = get_example_gds()
    print "long-term activity vector ('vertex': LT activity)"
    print phase_space_analysis.GetLTActivity(ps, gds1)


def main():
    visualization_example()
    sys.exit(0)
    # ---------------------------------------------
    LTActivity_example()
    sys.exit(0)
    # ---------------------------------------------
    activity_example()
    sys.exit(0)
    # ---------------------------------------------
    GoE_count_example()
    sys.exit(0)
    # ---------------------------------------------
    attractor_basin_count_example()
    sys.exit(0)
    # ---------------------------------------------
    max_transient_length_example()
    sys.exit(0)
    # ---------------------------------------------



# ------------------------------------------------------------
if __name__ == "__main__":
    main()
