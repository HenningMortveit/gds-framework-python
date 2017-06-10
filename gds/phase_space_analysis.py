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

# returns list of per. pts.
# ordered by weight of cycle (binary sum)
def GetPerCyclesList(ps):
    periodicPoints = ps.GetPeriodicPoints()

    periodicCycles = []
    for cycle in periodicPoints:
        perCyc = []
        for point in cycle:
            perCyc.append(point)
        periodicCycles.append(perCyc)

    for cycle in periodicCycles:
        cycle.insert(0, sum(cycle))

    periodicCycles.sort()
    for cycle in periodicCycles:
        cycle.pop(0)

    return periodicCycles

# outputs dictionary in the form:
# 'representative state in n-cycle(length of n-cycle)': length of longest transient
def GetMaxTransientLength(ps, gds):
    ps.GenerateDigraph()
    piDigraph = ps.GetDigraph()

    periodicCycles = GetPerCyclesList(ps)

    max = [0] * len(periodicCycles)
    per_pts_dict = {}

    for node in piDigraph.nodes():
        if (piDigraph.predecessors(node) == []):
            i = 0
            while i < len(periodicCycles):
                for point in periodicCycles[i]:
                    try:
                        path = nx.shortest_path(piDigraph, source=node, target=point)
                        if path[-2] not in periodicCycles[i]:
                            if len(path) > max[i]:
                                max[i] = len(path)
                    except nx.NetworkXNoPath:
                        break
                i += 1

    i = 0
    while i < len(max) :
        cycle_len = len(periodicCycles[i])
        perPt = gds.IntegerToState(periodicCycles[i][0])
        perPt_Str = gds.StateToString(perPt)
        perPt_Str += '(' + str(cycle_len) + ')'
        per_pts_dict[perPt_Str] = max[i]
        i += 1

    return per_pts_dict

# outputs dictionary in the form:
# 'representative state in n-cycle(length of n-cycle)': no. of states in cycle basin
def GetCycleBasinCount(ps,gds):
    ps.GenerateDigraph()
    piDigraph = ps.GetDigraph()

    periodicCycles = GetPerCyclesList(ps)
    per_pts_dict = {}

    for cycle in periodicCycles:
        cycle_len = len(cycle)
        per_pts_dict[cycle[0]] = cycle_len

    for component in nx.algorithms.weakly_connected_components(piDigraph):
        for state in component:
            if state in per_pts_dict.keys():
                perPt = gds.IntegerToState(state)
                perPt_Str = gds.StateToString(perPt)
                perPt_Str += '(' + str(per_pts_dict[state]) + ')'

                per_pts_dict[state] = len(component)
                per_pts_dict[perPt_Str] = per_pts_dict.pop(state)

    return per_pts_dict

# outputs dictionary in the form:
# 'representative state in n-cycle(length of n-cycle)': no. of GoE states in cycle basin
def GetGOECount(ps,gds):
    ps.GenerateDigraph()
    piDigraph = ps.GetDigraph()

    periodicCycles = GetPerCyclesList(ps)
    per_pts_dict = {}

    for cycle in periodicCycles:
        cycle_len = len(cycle)
        per_pts_dict[cycle[0]] = cycle_len

    for component in nx.algorithms.weakly_connected_components(piDigraph):
        goeCount = 0
        perPt_Str = 0
        for state in component:
            if state in per_pts_dict.keys():
                perPt = gds.IntegerToState(state)
                perPt_Str = gds.StateToString(perPt)
                perPt_Str += '(' + str(per_pts_dict[state]) + ')'

                per_pts_dict[state] = len(component)
                per_pts_dict[perPt_Str] = per_pts_dict.pop(state)
            if (piDigraph.predecessors(state) == []):
                goeCount += 1

        per_pts_dict[perPt_Str] = goeCount

    return per_pts_dict

def GetActivity(ps,gds):
    Graph = gds.g
    ps.GenerateDigraph()

    node_activity_dict = {}

    for node in Graph.nodes():
        node_activity = ps.ComputeActivity(node)
        node_activity_dict[str(node)] = node_activity

    return node_activity_dict

#Long-Term (LT) Activity
def GetLTActivity(ps,gds):
    Graph = gds.g
    ps.GenerateDigraph()

    node_LTactivity_dict = {}

    for node in Graph.nodes():
        node_LTactivity = ps.ComputeLTActivity(node)
        node_LTactivity_dict[str(node)] = node_LTactivity

    return node_LTactivity_dict