#
# This file is a part of the GDS python library named gds. Copyright,
# Henning S. Mortveit 2010.
#

import sequence

import copy

import networkx as nx
import networkx.algorithms


def NuFunction(orientation, cycle) :
    """Compute the value of the nu-function for the given orientation
    and the given cycle. It is assumed that cycle is valid."""

    nu = 0;
    n = len(cycle)

    for i in range(0, n):
        e = [cycle[i], cycle[(i+1) % n]]
        try :
            if e == orientation( e ) :
                nu += 1
            else :
                nu -= 1
        except :
            print "e, o(e):", e, orientation(e)

    return nu


def NuFunctionCB(orientation, cycleBasis ) :
    """Compute the value of the nu-function for the given orientation
    on the given cycle basis. It is assumed that cycle basis is
    valid."""

    nu = []
    for cycle in cycleBasis :
        nu.append( NuFunction(orientation, cycle) )

    return nu

def AutXActionAcycX(gamma, O) :
    """Return gamma dot O. Here gamma is an automorphism of the graph
    of O."""

    gammaInv = ~gamma
    digraph = networkx.DiGraph()

    for e in O.rep :
        gamma_e = [ gammaInv[e[0]], gammaInv[e[1]] ]
        O_gamma_e = O( gamma_e )
        edge = [ gamma[O_gamma_e[0]], gamma[O_gamma_e[1]] ]
        digraph.add_edge( edge[0], edge[1] )

    return Orientation( digraph = digraph )


class Orientation :

    def __init__(self, \
                     digraph     = None, \
                     graph       = None, \
                     orientation = None, \
                     permutation = None ) :

        """Here graph and digraph are undirected and directed graphs
        that have the networkx interface. One will either specify

            (i) a directed graph where (a,b) present implies (b,a) not
                 present.

            (ii) a graph *and* and orientation vector of length the
                 number of edges in the graph. Here 0 means oriented
                 by order and 1 oriented opposite of order.

            (iii) a graph *and* a permutation of length the number of
                 vertices in the graph.

        """

        self.rep = []

        self.graph = graph
        self.digraph = digraph
        self.permutation = permutation
        self.orientation = orientation

        self.CreateOrientation()


    def CreateOrientation(self) :

        if self.digraph != None :

            self.graph = None
            self.permutation = None
            self.orientation = None
            for e in sorted( self.digraph.edges() ) :
                self.rep.append( [e[0], e[1]] )
            return

        elif self.graph != None :

            if self.orientation == None and self.permutation == None :
                print "Must specify orientation list or permutation."
                raise Exception()

            edges = self.graph.edges()
            self.graph = None
            self.rep = []

            if self.orientation != None :
                for i, e in enumerate(edges) :
                    if self.orientation[i] == 0 :
                        self.rep.append( [e[0], e[1]] )
                    else :
                        self.rep.append( [e[1], e[0]] )
            elif self.permutation != None :
                pO = sequence.PermutationOrder(self.permutation)
                for e in edges :
                    if pO.LessThan( e[0], e[1] ) :
                        self.rep.append( [e[0], e[1]] )
                    else :
                        self.rep.append( [e[1], e[0]] )

            else :
                print "Missing case in create orientation"
                raise Exception()

            self.rep.sort()
            self.digraph = networkx.DiGraph( self.rep )

            return


    def __eq__(self, other) :
        return self.rep == other.rep


    def SetOrientation(graph, o) :

        if len( graph.edges() ) != len( o ) :
            print "Mismatch in SetOrientation"
            raise Exception()

        self.graph = graph
        self.orientation = o
        self.permutation = None
        self.digraph = None
        self.rep = []

        self.CreateOrientation()


    def InducedOrientation(graph, pi) :

        if len( graph.nodes() ) != len( pi ) :
            print "Mismatch in InducedOrientation"
            raise Exception()

        self.graph = graph
        self.orientation = None
        self.permutation = pi
        self.digraph = None
        self.rep = None

        self.CreateOrientation()



    def ClickConvert(self, v) :
        """Reverse orientation of all edges incident with 'v'."""

        for edge in self.rep :
            if v in edge :
                v0 = edge[0]
                v1 = edge[1]
                edge[0] = v1
                edge[1] = v0

        self.rep.sort()
        self.digraph = networkx.DiGraph( self.rep )

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
        if [edge[0], edge[1]] in self.rep :
            return [edge[0], edge[1]]
        elif [edge[1], edge[0]] in self.rep :
            return [edge[1], edge[0]]
        else :
            print "Edge not present in graph:", edge, self.rep
            raise Exception()


    def LinearExtension(self) :
        return nx.algorithms.topological_sort( self.digraph )

    def IsSource(self, v) :
        return self.digraph.in_degree(v) == 0
