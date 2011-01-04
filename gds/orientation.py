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

    def __eq__(self, other) :
        return self.digraph.edges() == other.digraph.edges()

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

    def ClickConvert(self, v) :
        """Reverse orientation of all edges incident with 'v'."""

        out_edges = self.digraph.out_edges(v)
        in_edges = self.digraph.in_edges(v)

        self.digraph.remove_edges_from(out_edges)
        self.digraph.remove_edges_from(in_edges)

        for e in out_edges :
            self.digraph.add_edge( e[1], e[0] )

        for e in in_edges :
            self.digraph.add_edge( e[1], e[0] )


    def GetSources(self) :
        """Return a list of source vertices, if any."""

        sources = []
        for i in self.digraph.nodes() :
            if self.digraph.in_degree( i ) == 0 :
                sources.append(i)

        return sources


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
