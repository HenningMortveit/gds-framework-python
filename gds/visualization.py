import sys
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
import gds
import algorithms
import equivalence
import util.enumeration

# cyclically shift pi-sequence to the left n times
def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

# outputs visual phasespace graph of \Upgamma(F_\pi)
# and shifted
def Output_PS_Figures(gds, pi, s):
    # initialize sequence of local functions: F_n \circ ... \circ F_1
    pi_seq = []
    for i in range(0, s):
        pi_seq.append(pi[i])

    # save transitions from applying local function seq.
    gds.SetSequence(pi_seq)
    transitions = algorithms.GenerateTransitions(gds)
    shift_transitions = []
    for x, y in enumerate(transitions):
        x1 = gds.IntegerToState(x)
        y1 = gds.IntegerToState(y)
        # print gds.StateToString(x), "->", gds.StateToString(y)
        shift_transitions.append(y)

    # graph non-shifted phase space, phase_space_figure.pdf
    gds.SetSequence(pi)
    ps = phase_space.PhaseSpace(gds, shift_transitions)
    ps.phase_space_figure()
    phase_space_figure = ps.GetDigraph()

    # cannot draw graphs with selfloops!
    se = phase_space_figure.selfloop_edges()
    phase_space_figure.remove_edges_from(se)

    A = nx.drawing.nx_agraph.to_agraph(phase_space_figure)
    A.layout(prog='neato', args="-Goverlap=false ")
    A.draw('phase_space_figure.pdf')
    subprocess.Popen('phase_space_figure.pdf', shell=True)  # automatically open .pdf file

    # saved transitions from applying local function seq.
    ps.shifted_phase_space_figure()
    shift_transition_digraph = ps.GetDigraph()

    # make shifted_phase_space_figure
    shifted_Pi = shift(pi, s)
    gds.SetSequence(shifted_Pi)
    ps = phase_space.PhaseSpace(gds)
    ps.phase_space_figure()
    shifted_phase_space_figure = ps.GetDigraph()

    # paint coinciding shifted edges/nodes
    num_edges = len(shifted_phase_space_figure.edges())
    hit_ratio = 0
    for edge in shifted_phase_space_figure.edges():
        # paint nodes and edge
        if edge in shift_transition_digraph.edges():
            shifted_phase_space_figure.add_edge(*edge, color="red")
            shifted_phase_space_figure.add_node(edge[0], color="red")
            shifted_phase_space_figure.add_node(edge[1], color="red")
            hit_ratio += 1
    # no. of painted states / no. of total states = hit_ratio
    hit_ratio /= float(num_edges)

    se = shifted_phase_space_figure.selfloop_edges()
    shifted_phase_space_figure.remove_edges_from(se)
    A = nx.drawing.nx_agraph.to_agraph(shifted_phase_space_figure)
    A.layout(prog='neato', args="-Goverlap=false ")
    A.draw('shifted_phase_space_figure.pdf')
    subprocess.Popen('shifted_phase_space_figure.pdf', shell=True)

    return hit_ratio

