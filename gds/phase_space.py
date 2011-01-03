#
#
#

import algorithms
import networkx as nx
import networkx.algorithms

class PhaseSpace :

    def __init__(self, gds) :
        self.gds = gds
        self.graph = None
        self.transitions = None
        self.fixedPoints = None
        self.periodicPoints = None
        self.components = None
        pass

    def Invalidate(self) :
        self.transitions = None
        self.graph = None
        self.fixedPoints = None
        self.periodicPoints = None
        self.components = None

    def GenerateTransitions(self) :
        self.Invalidate()

        self.graph = None
        self.transitions = algorithms.GenerateTransitions(self.gds)
        return self.transitions

    def GenerateDigraph(self) :
        if self.transitions == None :
            self.GenerateTransitions(gds)

        self.graph = nx.DiGraph()
        for i, j in enumerate( self.transitions ) :
            self.graph.add_edge(i, j)

    def GetTransitions(self) :
        return self.transitions

    def GetDigraph(self) :
        return self.graph

    def GetPeriodicPoints(self) :
        if self.periodicPoints == None :
            self.GeneratePeriodicPoints()
        return self.periodicPoints

    def GeneratePeriodicPoints(self) :
        if self.graph == None :
            self.GenerateDigraph()
        self.periodicPoints = nx.algorithms.attracting_components(self.graph)

    def GetFixedPoints(self) :
        if self.fixedPoints == None :
            self.GenerateFixedPoints()
        return self.fixedPoints

    def GenerateFixedPoints(self) :
        if self.transitions == None :
            self.GenerateTransitions()
        self.fixedPoints = algorithms.FixedPoints(self.gds,
                                                  self.transitions)

    def GetComponents(self) :
        if self.components == None :
            self.GenerateComponents()
        return self.components

    def GenerateComponents(self) :
        if self.graph == None :
            self.GenerateDigraph()
        self.components = nx.algorithms.weakly_connected_components(self.graph)
