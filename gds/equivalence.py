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


def AcyclicOrientations(graph):
    """Create all acyclic orientations of a graph by checking each
    possible edge orientation assignment."""
    acyclicOrientations = []
    linearExtensions = []

    m = len(graph.edges())
    enum = util.enumeration.NTupleGenerator(m * [2])
    N = enum.Num()

    for i in range(0, N):
        o = enum.Current()
        O = orientation.Orientation(graph=graph, orientation=o)

        try:
            le = O.LinearExtension()
            if le != None:
                acyclicOrientations.append(O)
                linearExtensions.append(le)
        except:
            pass

        enum.Next()

    return (acyclicOrientations, linearExtensions)


def LinearExtensions(graph):
    """Create a complete set of representatives of ~X equivalent
    linear extensions of a graph. The function AcyclicOrientations
    gives both the acyclic orientations and a set of linear
    extensions."""

    linExt = []

    m = len(graph.edges())

    # The empty graph: one linear extension
    if m == 0:
        linExt.append(range(0, graph.number_of_nodes()))
        return linExt

    enum = util.enumeration.NTupleGenerator(m * [2])
    N = enum.Num()

    for i in range(0, N):
        o = enum.Current()
        O = orientation.Orientation(graph=graph, orientation=o)

        try:
            le = O.LinearExtension()
            if le != None:
                linExt.append(le)
        except:
            pass

        enum.Next()

    return linExt


def KappaLinearExtensions(graph, v):
    """Create a transversal of linear extensions for the kappa classes
    of a graph. It is based on the fact that for each vertex v the set
    of acyclic orientations where v is the unique source is a
    transversal. The most efficient computation will result if v is
    chosen as a vertex of maximal degree."""

    if not graph.has_node(v):
        print "okay, the node specified is not in the graph."
        raise Exception()

    g = copy.deepcopy(graph)
    g.remove_node(v)


    (acycOrien, linExt) = AcyclicOrientations(g)

    kappaExt = []

    for i, le in enumerate(linExt):

        # append disconnected vertices
        pts = list(set(g.nodes()) - set(le))
        le.extend(pts)

        # Skip those orientations containing source vertices that are
        # not connected to v in the original graph.

        flag = False

        for j in graph.nodes():
            if j != v and \
                    (not graph.has_edge(j, v)) and \
                    acycOrien[i].IsSource(j):
                flag = True
                break

        if not flag:
            le.insert(0, v)
            kappaExt.append(le)

    return kappaExt


def KappaClasses(graph):
    """Compute the complete set of kappa classes (and not only
    representatives). Returns matching pairs of acyclic orientation
    and linear extensions."""

    kappaEqClasses = []

    X = networkx.Graph()

    (acyc, linExt) = AcyclicOrientations(graph)

    n = len(acyc)

    X.add_nodes_from(range(0, n))

    for i in range(0, n):
        sources = acyc[i].GetSources()
        for j in sources:
            acyc[i].ClickConvert(j)
            r = -1
            for k in range(0, n):
                if k != i and acyc[i] == acyc[k]:
                    r = k;
                    break
            # r = [(k, a2) for k, a2 in enumerate(acyc) if a == a2 and i != k ]
            acyc[i].ClickConvert(j)
            # if len(r) == 0 :
            if r == -1:
                print "What?? r = ", r
                print "source vertex: ", j
                print "sources:", sources
                print acyc[i].rep
                acyc[i].ClickConvert(j)
                print acyc[i].rep
                acyc[i].ClickConvert(j)
                print acyc[i].rep
                raise Exception()
            #            X.add_edge(i, r[0][0])
            X.add_edge(i, r)

    components = networkx.connected_components(X)

    for component in components:
        eqClass = []

        for k in component:
            eqClass.append([acyc[k], linExt[k]])

        kappaEqClasses.append(eqClass)

    return kappaEqClasses


def KappaBarClasses(graph, autX, kappaEqClasses=None):
    """Compute the kappa-bar classes of a graph. The argument 'group'
    should be the automorphism group of the 'graph'. One may re-use
    kappaEqClasses from earlier computations."""

    barClasses = []

    if kappaEqClasses == None:
        kappaEqClasses = KappaClasses(graph)

    cycleBasis = networkx.cycle_basis(graph, 0)

    kappa = len(kappaEqClasses)

    nu = []

    for eqClass in kappaEqClasses:
        nu.append(orientation.NuFunctionCB(eqClass[0][0], cycleBasis))

    X = networkx.Graph()

    for i, eqClass in enumerate(kappaEqClasses):
        O = eqClass[0][0]
        for gamma in autX:
            oPrime = orientation.AutXActionAcycX(gamma, O)
            nuPrime = orientation.NuFunctionCB(oPrime, cycleBasis)
            index = [j for j, nu_j in enumerate(nu) if nu_j == nuPrime]
            if len(index) > 0:
                X.add_edge(i, index[0])

    components = networkx.connected_components(X)

    for component in components:
        print "Type of index:", type(component)
        index = component[0]
        barClasses.append(kappaEqClasses[index][0])

    return barClasses


def AlphaBarClasses(graph, autX):
    """Compute the alpha-bar classes of a graph. The argument 'group'
    should be the automorphism group of the 'graph'."""

    acyc = AcyclicOrientations(graph)[0]

    X = networkx.Graph()

    for i, a in enumerate(acyc):
        for gamma in autX:
            aPrime = orientation.AutXActionAcycX(gamma, a)
            for j, ac in enumerate(acyc):
                if ac == aPrime:
                    X.add_edge(i, j)
                    break

    components = networkx.connected_components(X)

    barClasses = []

    for component in components:
        index = component[0]
        barClasses.append(acyc[index])

    return barClasses


# Enumeration

def ContractEdge(graph, e):
    """In the graph 'graph' contract the edge e to a vertex. Also
    return the edges inserted and the edges deleted. """

    i = e[0]
    j = e[1]

    deleteEdgeList = []
    insertEdgeList = []

    nBors = graph.neighbors(j)

    for k in nBors:
        deleteEdgeList.append((j, k))

        if k != i and (not graph.has_edge(i, k)):
            graph.add_edge(i, k)
            insertEdgeList.append((i, k))

    graph.remove_node(j)

    return (j, deleteEdgeList, insertEdgeList)


def RestoreContractedEdge(graph, j, deleteEdgeList, insertEdgeList):
    """Restore what ContractEdge did."""
    graph.add_node(j)
    graph.add_edges_from(deleteEdgeList)
    graph.remove_edges_from(insertEdgeList)


def EnumAcyclicOrientations(graph):
    """Standard recursion relation using deletion/contraction."""

    edges = graph.edges()
    m = len(edges)

    if m == 0:
        return 1
    if m == 1:
        return 2
    if m == 2:
        return 4

    edges = [list(i) for i in edges]
    e = edges[0]

    (j, deleteEdgeList, insertEdgeList) = ContractEdge(graph, e)
    k1 = EnumAcyclicOrientations(graph)
    RestoreContractedEdge(graph, j, deleteEdgeList, insertEdgeList)

    graph.remove_edge(e[0], e[1])
    k2 = EnumAcyclicOrientations(graph)
    graph.add_edge(e[0], e[1])

    return k1 + k2


def EnumKappaClasses(graph):
    """Compute the number of kappa classes of the graph 'graph' using
    the deletion contraction recursion with cycle edges."""

    m = len(graph.edges())

    if m == 0 or m == 1 or m == 2:
        return 1

    cycle_basis = networkx.cycle_basis(graph)
    if len(cycle_basis) == 0:
        return 1

    edge = [cycle_basis[0][0], cycle_basis[0][1]]

    (j, deleteEdgeList, insertEdgeList) = ContractEdge(graph, edge)
    k1 = EnumKappaClasses(graph)
    RestoreContractedEdge(graph, j, deleteEdgeList, insertEdgeList)

    graph.remove_edge(edge[0], edge[1])
    k2 = EnumKappaClasses(graph)
    graph.add_edge(edge[0], edge[1])

    return k1 + k2


def EnumAlphaBarClasses(graph, autX):
    """Compute the number of alpha-bar classes of a graph. The
    argument 'group' should be the automorphism group of the
    'graph'. This is the basic version using Burnside's lemma without
    reference to orbit graphs."""

    acyc = AcyclicOrientations(graph)[0]

    X = networkx.Graph()

    sum = 0

    for gamma in autX:

        for a in acyc:
            aPrime = orientation.AutXActionAcycX(gamma, a)
            if a == aPrime:
                sum += 1

    return sum / len(autX)


if __name__ == '__main__':
    import graphs
    import groups
    import biographs

    vpc = biographs.VPC(2, 0)
    g = vpc.GetGraph()
    n = g.selfloop_edges()
    g.remove_edges_from(n)

    alpha = EnumAcyclicOrientations(g.to_undirected())
    print "alpha", alpha

    kappa = EnumKappaClasses(g.to_undirected())
    print "kappa =", kappa

    sys.exit(0)

    q23 = graphs.HyperCube(dim=2, base=2)
    autq23 = groups.CreateAutQ2_3()

    kappa = EnumKappaClasses(q23)
    print "kappa(q23) =", kappa
    alpha = EnumAcyclicOrientations(q23)
    print "alpha(q23) =", alpha
    #    alphaBar = len( AlphaBarClasses(q23, autq23) )
    alphaBar = EnumAlphaBarClasses(q23, autq23)
    print "alphaBar(q23) =", alphaBar
