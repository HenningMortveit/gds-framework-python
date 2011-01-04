#
# This file is a part of the GDS python library named gds. Copyright,
# Henning S. Mortveit 2010.
#

import util.enumeration
import sequence
import orientation
import copy
import networkx
import sys

def AcyclicOrientations(graph) :
    """Create all acyclic orientations of a graph by checking each
    possible edge orientation assignment."""

    acyclicOrientations = []
    linearExtensions = []

    m = len( graph.edges() )
    enum = util.enumeration.NTupleGenerator( m * [2] )
    N = enum.Num()

    for i in range(0, N) :
        o = enum.Current()
        O = orientation.Orientation(graph, orientation = o)
        try :
            le = O.LinearExtension()
            if le != None :
                acyclicOrientations.append(O)
                linearExtensions.append(le)
        except :
            pass

        enum.Next()

    return (acyclicOrientations, linearExtensions)


def KappaClasses(graph) :
    """Compute the complete set of kappa classes (and not only
    representatives)."""

    kappaEqClasses = []

    X = networkx.Graph()

    (acyc, linExt) = AcyclicOrientations(graph)

    n = len( acyc )
    X.add_nodes_from( range(0,n) )

    for i, a in enumerate(acyc) :
        sources = a.GetSources()
        for j in sources :
            a.ClickConvert(j)
            r = [(k, a2) for k, a2 in enumerate(acyc) if a == a2 and i != k ]
            a.ClickConvert(j)
            X.add_edge(i, r[0][0])

    components = networkx.connected_components(X)

    for component in components :
        eqClass = []

        for k in component :
            eqClass.append( [acyc[k], linExt[k] ] )

        kappaEqClasses.append( eqClass )

    return kappaEqClasses



def LinearExtensions(graph) :
    """Create a complete set of representatives of ~X equivalent
    linear extensions of a graph. The function AcyclicOrientations
    gives both the acyclic orientations and a set of linear
    extensions."""

    linExt = []

    m = len( graph.edges() )

    enum = util.enumeration.NTupleGenerator( m * [2] )
    N = enum.Num()

    for i in range(0, N) :
        o = enum.Current()
        O = orientation.Orientation(graph, orientation = o)
        try :
            le = O.LinearExtension()
            if le != None :
                linExt.append( le )
        except :
            pass

        enum.Next()

    return linExt


def KappaLinearExtensions(graph, v) :
    """Create a transversal of linear extensions for the kappa classes
    of a graph. It is based on the fact that for each vertex v the set
    of acyclic orientations where v is the unique source is a
    transversal. The most efficient computation will result if v is
    chosen as a vertex of maximal degree."""

    if not graph.has_node(v) :
        print "okay, the node specified is not in the graph."
        raise Exception()

    g = copy.deepcopy(graph)
    g.remove_node(v)

    (acycOrien, linExt) = AcyclicOrientations(g);

    kappaExt = []

    for i, le in enumerate(linExt) :

        # Skip those orientations containing source vertices that are
        # not connected to v in the original graph.

        flag = False

        for j in graph.nodes() :
            if j != v and \
                    (not graph.has_edge( j, v )) and \
                    acycOrien[i].IsSource( j ) :

                flag = True
                break

        if not flag :
            le.insert(0, v)
            kappaExt.append(le)

    return kappaExt



def ContractEdge(graph, e) :
    """In the graph 'graph' contract the edge e to a vertex. Also
    return the edges inserted and the edges deleted. """

    i = e[0]
    j = e[1]

    deleteEdgeList = []
    insertEdgeList = []

    nBors = graph.neighbors(j)

    for k in nBors :
        deleteEdgeList.append( (j,k) )

        if k != i and (not graph.has_edge(i,k) ) :
            graph.add_edge(i,k)
            insertEdgeList.append( (i,k) )

    graph.remove_node(j)

    return (j, deleteEdgeList, insertEdgeList)


def RestoreContractedEdge(graph, j, deleteEdgeList, insertEdgeList) :
    """Restore what ContractEdge did."""
    graph.add_node(j)
    graph.add_edges_from( deleteEdgeList )
    graph.remove_edges_from( insertEdgeList )


def EnumAcyclicOrientations(graph) :
    """Standard recursion relation using deletion/contraction."""

    edges = graph.edges();
    m = len(edges)

    if m == 0 :
        return 1
    if m == 1 :
        return 2
    if m == 2 :
        return 4

    e = edges[0]

    (j, deleteEdgeList, insertEdgeList) = ContractEdge(graph, e)
    k1 = EnumAcyclicOrientations(graph)
    RestoreContractedEdge(graph, j, deleteEdgeList, insertEdgeList)

    graph.remove_edge(e[0], e[1])
    k2 = EnumAcyclicOrientations(graph)
    graph.add_edge(e[0], e[1])

    return k1 + k2
