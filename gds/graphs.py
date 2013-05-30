#
# This module has functions for creating some standard graph
# classes. Graphs are based on the networkx library. All graphs are
# assumed to have vertex set {0,1, 2, n} for some suitable n.
#

import copy
import networkx
import util.enumeration

def CircleGraph(n) :
    """Create and return undirected circle graph on n vertices."""

    X = networkx.Graph()
    X.add_nodes_from( range(0,n) )
    for i in range(0, n) :
        X.add_edge( i, (i+1) % n )
    return X


def GeneralCircleGraph(n,r) :
    """Create and return the undirected, generalized circle graph on n
    vertices where each vertex is connected to all neighbors of
    distance <= r.
    """

    X = CircleGraph(n)
    for i in range(0, n) :
        for j in range(2, r+1) :
            X.add_edge( i, (i+j) % n )
    return X


def PathGraph(n) :
    """Create and return undirected path graph on n vertices."""

    X = networkx.Graph()
    for i in range(0, n-1) :
        X.add_edge( i, (i+1) )
    return X

def StarGraph(n) :
    """Create and return the star graph with 0 as center vertex and 1
    through n as satellite vertices."""

    X = networkx.Graph()

    for i in range(1, n+1) :
        X.add_edge(0,i)

    return X


def WheelGraph(n) :
    """Create and return the wheel graph with 0 as center vertex and 1
    through n as rim vertices."""

    X = StarGraph(n)

    for i in range(1, n) :
        X.add_edge(i, i+1)
    X.add_edge(1, n)

    return X


def HammingDistance( v1, v2 ) :
    if len(v1) != len(v2) :
        print "Dimension mismatch"
        raise Exception

    sum = 0
    for i, v in enumerate(v1) :
        if v != v2[i] :
            sum += 1

    return sum

def HyperCube(dim = 3, base = 2) :
    """Create the hypercube of dimension dim and the given base"""

    limits = dim * [base]

    ng = util.enumeration.NTupleGenerator(limits)
    N = ng.Num()
    vertexList = []

    for i in range(0, N) :
        vertexList.append( copy.copy(ng.Current()) )
        ng.Next()

    X = networkx.Graph()

    for i in range(0, N) :
        for j in range(i+1, N) :
            if HammingDistance( vertexList[i], vertexList[j] ) == 1 :
                X.add_edge(i,j)

    return X
