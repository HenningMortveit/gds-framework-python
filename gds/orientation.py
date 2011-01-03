#
# This file is a part of the GDS python library named gds. Copyright,
# Henning S. Mortveit 2010.
#

import sequence

import networkx as nx
import networkx.algorithms

class Orientation :

    def __init__(self, graph, orientation = None, pi = None) :
        """graph is an undirected graph that has the networkx
        interface. orientation is a list of 0/1 of length the number
        of edges in graph."""

        if orientation == None and pi == None :
            print "Must specify orientation list or permutation."
            raise Exception()

        self.graph = graph
        self.orientation = orientation
        self.pi = pi
        self.digraph = None
        self.CreateOrientation()

    def SetOrientation(o) :

        if len( self.graph.nodes() ) != len( o ) :
            print "Mismatch"
            raise Exception()

        self.orientation = o
        self.pi = None

        self.CreateOrientation()


    def InducedOrientation(pi) :

        if len( self.graph.nodes() ) != len( pi ) :
            print "Mismatch"
            raise Exception()

        self.orientation = None
        self.pi = pi

        self.CreateOrientation()


    def CreateOrientation(self) :
        edges = self.graph.edges()
        self.digraph = networkx.DiGraph()

        if self.orientation != None :
            for i, e in enumerate(edges) :
                if self.orientation[i] == 0 :
                    self.digraph.add_edge( e[0], e[1] )
                else :
                    self.digraph.add_edge( e[1], e[0] )
        else :
            pO = sequence.PermutationOrder(self.pi)
            for e in edges :
                if pO.LessThan( e[0], e[1] ) :
                    self.digraph.add_edge( e[0], e[1] )
                else :
                    self.digraph.add_edge( e[1], e[0] )

    def IsAcyclic(self) :
        pi = nx.algorithms.topological_sort( self.digraph )
        if pi == None :
            return False
        else :
            return True

    def __call__(self, edge) :
        if not self.graph.has_edge( edge[0], edge[1] ) :
            print "Edge not present in graph"
            raise Exception()
        if self.digraph.has_edge( edge[0], edge[1] ) :
            return [edge[0], edge[1]]
        else :
            return [edge[1], edge[0]]
        pass

    def LinearExtension(self) :
        return nx.algorithms.topological_sort( self.digraph )

    def IsSource(self, v) :
        return self.digraph.in_degree(v) == 0
