#
#
#

import algorithms
import networkx as nx
import networkx.algorithms
import copy
class PhaseSpace:
    def __init__(self, gds, shift_transitions=None):
        # used in visualization.py
        if shift_transitions is None:
            shift_transitions = []

        self.gds = gds
        self.graph = None
        self.transitions = None
        self.fixedPoints = None
        self.periodicPoints = None
        self.components = None

        self.shift_transitions = shift_transitions

        self.activity = 0
        self.diff = 0

        self.ltactivity = 0
        self.ltdiff = 0

        self.iNode = None

        pass

    def Invalidate(self):
        self.transitions = None
        self.graph = None
        self.fixedPoints = None
        self.periodicPoints = None
        self.components = None

    def GenerateTransitions(self):
        self.Invalidate()

        self.graph = None
        self.transitions = algorithms.GenerateTransitions(self.gds)
        return self.transitions

    def shifted_phase_space_figure(self):
        if self.transitions == None:
            self.GenerateTransitions()
        self.graph = nx.DiGraph()
        for i, j in enumerate(self.transitions):
            xNewState = self.gds.IntegerToState(self.shift_transitions[i])
            yNewState = self.gds.IntegerToState(self.shift_transitions[j])
            self.graph.add_edge(self.gds.StateToString(xNewState), self.gds.StateToString(yNewState))

    def phase_space_figure(self):
        if self.transitions == None:
            self.GenerateTransitions()
        self.graph = nx.DiGraph()
        for x, y in enumerate(self.transitions):
            xNewState = self.gds.IntegerToState(x)
            yNewState = self.gds.IntegerToState(y)
            self.graph.add_edge(self.gds.StateToString(xNewState), self.gds.StateToString(yNewState))

    def GenerateDigraph(self):
        if self.transitions == None:
            self.GenerateTransitions()

        self.graph = nx.DiGraph()
        for i, j in enumerate(self.transitions):
            self.graph.add_edge(i, j)

    def GetTransitions(self):
        if self.transitions == None:
            self.GenerateTransitions()
        return self.transitions

    def GetDigraph(self):
        return self.graph

    def GetPeriodicPoints(self):
        if self.periodicPoints == None:
            self.GeneratePeriodicPoints()
        return self.periodicPoints

    #long-term (LT) activity
    def ComputeLTActivity(self, iNode):
        self.ltdiff = 0
        self.iNode = iNode
        self.GenerateComponents()
        for component in self.components:
            for x in component:
                state = self.gds.IntegerToState(x)
                iFlipState = state
                if (iFlipState[self.iNode].x == 0):
                    iFlipState[self.iNode].x = 1
                else:
                    iFlipState[self.iNode].x = 0
                iFlipStateIndex = self.gds.StateToInteger(iFlipState)
                if (iFlipStateIndex not in component):
                    self.ltdiff = self.ltdiff + 1
        self.ltactivity = float(self.ltdiff) / (self.gds.NumStates())
        return self.ltactivity

    def GeneratePeriodicPoints(self):
        if self.graph == None:
            self.GenerateDigraph()
        self.periodicPoints = nx.algorithms.attracting_components(self.graph)

    def GetFixedPoints(self):
        if self.fixedPoints == None:
            self.GenerateFixedPoints()
        return self.fixedPoints

    def GenerateFixedPoints(self):
        if self.transitions == None:
            self.GenerateTransitions()
        self.fixedPoints = algorithms.FixedPoints(self.gds,
                                                  self.transitions)

    def GetComponents(self):
        if self.components == None:
            self.GenerateComponents()
        return self.components

    def GenerateComponents(self):
        if self.graph == None:
            self.GenerateDigraph()
        self.components = nx.algorithms.weakly_connected_components(self.graph)

    def GetActivity(self):
        return self.activity

    def ComputeActivity(self, iNode):
        self.diff = 0
        self.iNode = iNode
        for x, y in enumerate(self.transitions):
            state = self.gds.IntegerToState(x)
            iFlipState = state
            if (iFlipState[self.iNode].x == 0):
                iFlipState[self.iNode].x = 1
            else:
                iFlipState[self.iNode].x = 0
            iFlipStateIndex = self.gds.StateToInteger(iFlipState)
            iFlipImageIndex = self.transitions[iFlipStateIndex]
            if (y != iFlipImageIndex):
                self.diff = self.diff + 1
        self.activity = float(self.diff) / (self.gds.NumStates())
        return self.activity
