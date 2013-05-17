
#import pygraphviz as pgv

import gds.util.enumeration
import gds.state
import gds.graphs
import gds.functions
import gds.gds
import gds.algorithms
import gds.state_algorithms
import gds.phase_space
import gds.sequence
import gds.equivalence
import gds.orientation
import gds.groups
import gds.sequence

import networkx as nx
from networkx.algorithms import *
import matplotlib.pyplot as plt

import math
import copy
import sys
import cProfile

def PlotExample() :
    X = networkx.Graph()
    X.add_edge( 0, 1);
    X.add_edge( 0, 2);
    X.add_edge( 1, 2);

    pos = dict();
    pos[0] = [0,0]
    pos[1] = [1,0]
    pos[2] = [1,1]

    networkx.drawing.nx_pylab.draw_networkx(X, pos=pos)
    plt.show()

def MakePNASNetwork() :
    X = networkx.Graph()
    edges = [
        (1,2), (1,3),
        (2,8), (2,10),
        (3,4), (3,10),
        (4,5), (4,9),
        (5,7), (5,8), (5,10),
        (6,7), (6,9), (6,10), (6,11),
        (7,8), (7,9), (7,10), (7,11),
        (8,9), (8,10), (8,11),
        (9,10),
        (10,11)
        ]
    for e in edges :
        X.add_edge(e[0], e[1])
    return X


def BiThresholdExample() :

    n = 4
    pi = [0,1,2,3];
    X = gds.graphs.CircleGraph(n)
    doCircle = True
#    X = gds.graphs.WheelGraph(n-1)
#    X = gds.graphs.HyperCube(dim = 3, base = 2)
    f = n * [gds.functions.biThreshold(1,3)]
#    one  = gds.state.State(1, 2)
#    zero = gds.state.State(0, 2)

#     s = [one,zero,zero]
#     i = [0,1,2]
#     print f[0](s,i,1)
#     sys.exit(0)

    stateObject = n * [gds.state.State(0, 2)]


    gds1 = gds.gds.GDS(X, f, stateObject, doCircle)
    gds1.SetSequence(pi)
#    gds1.SetParallel()


    transitions = gds.algorithms.GenerateTransitions(gds1)
    fixedPoints = gds.algorithms.FixedPoints(gds1, transitions)

    p = gds.phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: "
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

    print "Periodic points: "
    for i, cycle in enumerate(periodicPoints) :
        print i
        for j in cycle :
            print gds1.IntegerToState(j)

    print "Components: ", components

    for x,y in enumerate(transitions) :
        print gds1.IntegerToState(x), "->", gds1.IntegerToState(y)

    return transitions

def DynThresholdExample() :

    n = 5

    X = gds.graphs.StarGraph(n)
    stateObject = (n+1) * [gds.state.StateDynT(0, 1, 1)]
    stateObject[0] = gds.state.StateDynT(0,1, n)

    f = (n+1) * [gds.functions.f_up_down]

    gds1 = gds.gds.GDS(X, f, stateObject, False)

    transitions = gds.algorithms.GenerateTransitions(gds1)
    fixedPoints = gds.algorithms.FixedPoints(gds1, transitions)

    p = gds.phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: %i" % len(fixedPoints)
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

def SDSExample() :
    """Basic example for phase space on X = Circle_4."""

    n = 4

    pi0 = [3,2,1,0]

    pi1 = [0,1,2,3,4,5]
    pi2 = [0,1,5,2,3,4]
    pi3 = [0,1,5,2,4,3]
    pi4 = [0,1,5,4,3,2]
    pi5 = [0,5,4,3,2,1]

    X = gds.graphs.CircleGraph(n)
    #f = n * [gds.functions.wolfram(110)]
    #f = n * [gds.functions.nor]
    f = n * [gds.functions.wolfram(240)]

#    one  = gds.state.State(1, 2)
#    zero = gds.state.State(0, 2)

#     s = [one,zero,zero]
#     i = [0,1,2]
#     print f[0](s,i,1)
#     sys.exit(0)

    stateObject = n * [gds.state.State(0, 2)]

    doCircle = True
    gds1 = gds.gds.GDS(X, f, stateObject, doCircle)
    gds1.SetSequence(pi0)

    transitions = gds.algorithms.GenerateTransitions(gds1)
    fixedPoints = gds.algorithms.FixedPoints(gds1, transitions)

    p = gds.phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: "
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

    print "Periodic points: "
    for i, cycle in enumerate(periodicPoints) :
        print i
        for j in cycle :
            print gds1.IntegerToState(j)

    print "Components: ", components

    for x,y in enumerate(transitions) :
        print gds1.IntegerToState(x), "->", gds1.IntegerToState(y)

    return transitions



def SDSBlockSequenceExample() :
    """Basic example for phase space on X = Circle_4."""

    n = 5

    pi0 = [[0,3], [4], [1], [2]]

    X = gds.graphs.CircleGraph(n)
    f = n * [gds.functions.nor]

    stateObject = n * [gds.state.State(0, 2)]

    doCircle = True
    gds1 = gds.gds.GDS(X, f, stateObject, doCircle)
    gds1.SetBlockSequence(pi0)

    transitions = gds.algorithms.GenerateTransitions(gds1)
    fixedPoints = gds.algorithms.FixedPoints(gds1, transitions)

    p = gds.phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: "
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

    print "Periodic points: "
    for i, cycle in enumerate(periodicPoints) :
        print i
        for j in cycle :
            print gds1.IntegerToState(j)

    print "Components: ", components

    for x,y in enumerate(transitions) :
        print gds1.IntegerToState(x), "->", gds1.IntegerToState(y)

    return transitions



def SDSExample3() :
    """Basic example for phase space on X = Circle_4."""

    n = 3

    pi1 = [0,1,2]

    #X = gds.graphs.CircleGraph(n)


    X = networkx.Graph()
    X.add_edge( 0, 1);
    X.add_edge( 0, 2);
    X.add_edge( 1, 2);


    f = n * [gds.functions.nand]

    stateObject = n * [gds.state.State(0, 2)]

    doCircle = True
    gds1 = gds.gds.GDS(X, f, stateObject, doCircle)
#    gds1.SetSequence(pi2)

    transitions = gds.algorithms.GenerateTransitions(gds1)
    fixedPoints = gds.algorithms.FixedPoints(gds1, transitions)

    p = gds.phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: "
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

    print "Periodic points: "
    for i, cycle in enumerate(periodicPoints) :
        print i
        for j in cycle :
            print gds1.IntegerToState(j)

    print "Components: ", components

    for x,y in enumerate(transitions) :
        print gds1.IntegerToState(x), "->", gds1.IntegerToState(y)

    return transitions



def SDSExample2() :
    """Basic example for phase space on X = Circle_4."""

    n = 4
    circ = gds.graphs.CircleGraph(n)
    #f = n * [gds.functions.wolfram(110)]
    f = n * [gds.functions.majority]
    stateObject = n * [gds.state.State(0, 2)]

    gds1 = gds.gds.GDS(circ, f, stateObject, True)
    le = gds.equivalence.LinearExtensions( circ )

    s = list()

    for pi in le :
        gds1.SetSequence(pi)
        transitions = gds.algorithms.GenerateTransitions(gds1)
        if not transitions in s :
            s.append(transitions)

    print len(s)
#    p = gds.phase_space.PhaseSpace(gds1)





def NetworkXExample(transitions) :
    """Example of how phase space can be manipulated by network x"""

    d = nx.DiGraph()
    for i in range(0, len(transitions) ) :
        d.add_edge(i,transitions[i])

    orbits = attracting_components(d)
    print "Periodic orbits: ", orbits

    components =  weakly_connected_components(d)
    print "Components: ", components

    return d



#import itertools

#for p in itertools.chain(itertools.permutations([0,1,2,3])) :
#    print p

def OrientationExample() :
    circ =  gds.graphs.CircleGraph(4)
    pi = gds.sequence.Permutation([0,1,2,3])
    aO = gds.orientation.Orientation(graph = circ, permutation = pi)

    print "Orientation", "{3,2}", aO( (3,2) )
    print "Orientation", "{2,3}", aO( (2,3) )
    print "Linear extension: ", aO.LinearExtension()



def FinalExam() :
    n = 7

    X = networkx.Graph()
    edges = [
        [0,1], [0,3], [0,5],
        [1,2], [1,6],
        [3,2], [3,4], [0,5],
        [5,4], [5,6]
        ]
    for e in edges :
        X.add_edge(e[0], e[1])

    print "Linear extensions:"
    le = gds.equivalence.LinearExtensions( X )
    for e in le :
        print "\t", e

    print "\talpha(Y) = ", len(le)

    print "Kappa representatives - linear extensions:"
    kle = gds.equivalence.KappaLinearExtensions(X, 0)
    for e in kle :
        print "\t", e

    print "\tkappa(Y) = ", len(kle)


    p1 = gds.sequence.Permutation( [0, 3, 4, 5, 6, 1, 2] )
    p2 = gds.sequence.Permutation( [0, 3, 2, 1, 6, 5, 4] )

    autX = gds.groups.ComputeGroup( [p1, p2] )


    print "Kappa bar representatives - linear extensions:"
    kble = gds.equivalence.KappaBarClasses(X, autX)
    for e in kble :
        print "\t", e[1]

    print "\tkappabar(Y) = ", len(kble)


    k = gds.equivalence.EnumAlphaBarClasses(X, autX)
    print "\talphabar(X) = ", k


def PhaseSpace() :
    """Basic example for phase space on X = Circle_4."""

    n = 4
    circ = gds.graphs.CircleGraph(n)
    f = n * [gds.functions.majority]
    stateObject = n * [gds.state.State(0, 2)]

    gds1 = gds.gds.GDS(circ, f, stateObject, True)

    phaseSpace = gds.phase_space.PhaseSpace(gds1);
    components = phaseSpace.GetComponents()
    print components
    fixedPoints = phaseSpace.GetFixedPoints();
    print fixedPoints
    periodicPoints = phaseSpace.GetPeriodicPoints()
    print periodicPoints

def NotEqual(a,b) : 
    return a!=b

def HammingDistance(x,y) :
    assert len(x) == len(y)
    return sum( map(NotEqual, x, y) )

def HammingNorm(x) :
    return HammingDistance(x, len(x)*[gds.state.State(0, 2)] )

def DerridaDiagram() :

    n = 5
    circ = gds.graphs.CircleGraph(n)
    f = n * [gds.functions.nor]
    stateObject = n * [gds.state.State(0, 2)]
    gds1 = gds.gds.GDS(circ, f, stateObject, True)

    phaseSpace = gds.phase_space.PhaseSpace(gds1);
    F = phaseSpace.GetTransitions()

    diagram = []
    for i in range(0, n+1) :
        diagram.append( (n+1)*[0] )

    n = gds1.GetDim();
    stateObjectList = gds1.stateObjectList
    limit = gds1.tupleConverter.limit
    ng = gds.util.enumeration.NTupleGenerator(limit)
    nStates = ng.Num()

    x = n*[0]
    y = n*[0]
    image_x = n*[0]
    image_y = n*[0]

    for i in xrange(0, nStates) :
        config = ng.Current()

        # Convert from index space to state space:
        for j in range(0,n) :
            x[j] = stateObjectList[j].IndexToState( config[j] )
        image_x =  gds1.tupleConverter.IndexToTuple( F[i] ) 

        ng2 = copy.deepcopy(ng)

        for j in xrange(i+1, nStates) :
            ng2.Next()
            config = ng2.Current()
            for k in range(0,n) :
                y[k] = stateObjectList[k].IndexToState( config[k] )

            hd = HammingDistance(x,y)
            image_y = ng.IndexToTuple( F[j] )
            hd2 = HammingDistance(image_x, image_y)
            diagram[hd][hd2] += 1
#            print x, y, hd, hd2

        ng.Next()

    return diagram


def StateSensitivity(gds1) :

    n = gds1.GetDim()

    phaseSpace = gds.phase_space.PhaseSpace(gds1);
    F = phaseSpace.GetTransitions()

    components = phaseSpace.GetComponents()
    compID = len(F) * [-1]
    for comp in range(0, len(components) ):
        for j in range(0, len(components[comp]) ) :
            compID[ components[comp][j] ] = comp

    N1_diagram = []
    for i in range(0, n+1) :
        N1_diagram.append( (n+1)*[0] )

    N2_diagram = []
    for i in range(0, n+1) :
        N2_diagram.append( (n+2)*[0] )

    N3_diagram = []
    for i in range(0, n+1) :
        N3_diagram.append( (n+1)*[0] )

    N4_diagram = []
    for i in range(0, n+1) :
        N4_diagram.append( (n+2)*[0] )

    n = gds1.GetDim();
    stateObjectList = gds1.stateObjectList
    limit = gds1.tupleConverter.limit
    ng = gds.util.enumeration.NTupleGenerator(limit)
    nStates = ng.Num()

    x = n*[0]
    y = n*[0]
    image_x = n*[0]
    image_y = n*[0]

    for i in xrange(0, nStates) :
        config = ng.Current()

        # Convert from index space to state space:
        for j in range(0,n) :
            x[j] = stateObjectList[j].IndexToState( config[j] )

        hn = HammingNorm(x)
        i_image = F[i] 
        i_comp = compID[i]

        dist = 0
        n2_set = set()
        n2_set.add(i_image)
        comp_dist = 0
        n4_set = set()
        n4_set.add(i_comp)

        for j in xrange(0, n) :

            x[j].x = (x[j].x+1) % 2
            for k in range(0,n) :
                y[k] = stateObjectList[k].StateToIndex( x[k] )
            x[j].x = (x[j].x+1) % 2

            index = gds1.tupleConverter.TupleToIndex(y)

            j_image = F[index]
            n2_set.add(j_image)
            n4_set.add( compID[index] )

            if i_image != j_image :
                dist += 1
            if i_comp != compID[index] :
                comp_dist += 1

        N1_diagram[hn][dist] += 1
        N2_diagram[hn][ len(n2_set) ] += 1
        N3_diagram[hn][ comp_dist ] += 1
        N4_diagram[hn][ len(n4_set) ] += 1
        ng.Next()
        print hn
        print "N2:", n2_set
        print "N4:", n4_set

    
    return N1_diagram, N2_diagram, N3_diagram, N4_diagram

def DiagTranspose(m) :
    nRows = len(m[0])
    nCols = len(m)
    M = []
    for i in range(0, nRows) :
        M.append( nCols*[0] )

    for i in range(0, nRows) :
        for j in range(0, nCols) :
            M[i][j] = m[j][i]

    return M

def ColumnNormalize(m) :
    M = copy.deepcopy(m)
    for i in range(0, len(M) ) :
        col = M[i]
        s = float( sum( col ) )
        if s == 0.0 :
            continue
        else :
            s = 1.0/s
            for j in range(0, len(col) ):
                col[j] *= s
                   
    return M


def ComputeStats( v ) :
    n = sum(v)
    avg = 0.0
    var = 0.0
    for i in range(0, len(v)) :
        avg += i*v[i]
        var += i*(v[i]*v[i])
    avg = avg/n
    var = var/n
    stdev = math.sqrt(var - avg*avg)
    return  avg, stdev

def ComputeAllStats( M ) :
    """Compute the average and standard deviation for each element of M"""
    
    s = []
    for i in range(0, len(M)) :
        s.append( [i, ComputeStats(M[i]) ] )
    return s



def main() :

    print ComputeStats( [2,2,4] )
    sys.exit(-1)

    n = 8
    circ = gds.graphs.CircleGraph(n)
    f = n * [gds.functions.majority]
    stateObject = n * [gds.state.State(0, 2)]
    gds1 = gds.gds.GDS(circ, f, stateObject, True)


    N1_diagram, N2_diagram, N3_diagram, N4_diagram = StateSensitivity(gds1)
    print N1_diagram
    print N2_diagram
    print N3_diagram
    print N4_diagram
    ddiag = DerridaDiagram()

    stats = ComputeAllStats( N1_diagram )

    plt.imshow(DiagTranspose( ColumnNormalize( ddiag) ), origin="lower")
    plt.gray()
    plt.colorbar()
    plt.show()


    sys.exit(0);



    DynThresholdExample()
    sys.exit(0)

    BiThresholdExample()
    sys.exit(0)



    SDSBlockSequenceExample()
    sys.exit(0)

    FinalExam();
    sys.exit(0);

    SDSExample3()
    sys.exit(0)


    SDSExample()
    sys.exit(0)


    X = MakePNASNetwork()
    X = gds.graphs.PathGraph(4)
    print X.edges()

    le = gds.equivalence.LinearExtensions( X )
    print len(le)
    for pi in le :
        print "\t", pi


    sys.exit(0)
    SDSExample2()

    transitions = SDSExample()
    NetworkXExample(transitions)
    OrientationExample()

    circ = gds.graphs.PathGraph(6)
    circ = gds.graphs.WheelGraph(4)
    q23 = gds.graphs.HyperCube(dim = 3, base = 2)
    circ = gds.graphs.CircleGraph(4)

    print "Circle:"
    print "\tVertices:", circ.nodes()
    print "\tEdges:", circ.edges()


    # Circle case

    n = 4

    c = gds.graphs.CircleGraph(n)
    d = gds.groups.D_n(n)

    print "circle graph:", n
    print "Linear extensions:"
    le = gds.equivalence.LinearExtensions( c )
    for e in le :
        print "\t", e

    print "Kappa representatives - linear extensions:"
    kle = gds.equivalence.KappaLinearExtensions(c, 0)
    for e in kle :
        print "\t", e

    print "Kappa bar representatives - linear extensions:"
    kble = gds.equivalence.KappaBarClasses(c, d)
    for e in kble :
        print "\t", e[1]

    print "Circle", n
    print "\talpha(Y) = ", len(le)
    print "\tkappa(Y) = ", len(kle)
    print "\tkappabar(Y) = ", len(kble)
    print ""

    # 3-cube

    q23 = gds.graphs.HyperCube(dim = 3, base = 2)
    autq23 = gds.groups.CreateAutQ2_3()

    le = gds.equivalence.LinearExtensions( q23 )
    for e in le :
        print "\t", e

    print "Kappa representatives - linear extensions:"
    kle = gds.equivalence.KappaLinearExtensions(q23, 0)
    for e in kle :
        print "\t", e

    print "Kappa bar representatives - linear extensions:"
    kble = gds.equivalence.KappaBarClasses(q23, autq23)
    for e in kble :
        print "\t", e[1]

    print "3-cube", n
    print "\talpha(Y) = ", len(le)
    print "\tkappa(Y) = ", len(kle)
    print "\tkappabar(Y) = ", len(kble)
    print ""

    #networkx.draw(q23)
    networkx.draw_graphviz(q23)
# ------------------------------------------------------------


main()

#cProfile.run('main()', 'profile.txt')
