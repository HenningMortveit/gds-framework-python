 
#import pygraphviz as pgv

import sys
sys.path += ["/Users/henning/git/gds"]
#sys.path += ["/Users/Sichao/gitlab/gds"]

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
import gds.sequence
import gds.groups

import networkx as nx
import copy
import gds.biographs

def UpdateSequenceEquivalenceExample() :

    # Circle case

    n = 4
    c = gds.graphs.CircleGraph(n)

#    circ = gds.graphs.PathGraph(6)
#    circ = gds.graphs.WheelGraph(4)

    print "Circle:"
    print "\tVertices:", c.nodes()
    print "\tEdges:", c.edges()

    d = gds.groups.D_n(n)

    # Linear extensions:
    le = gds.equivalence.LinearExtensions( c )
    print "Linear extensions: ", len(le)
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
    print "\talphabar(Y) = ", gds.equivalence.EnumAlphaBarClasses(c,d)
    print ""

#    print gds.equivalence.EnumAcyclicOrientations(c)
#    print gds.equivalence.EnumKappaClasses(c)

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

    print "Q_2^3"
    print "\talpha(Y) = ", len(le)
    print "\tkappa(Y) = ", len(kle)
    print "\tkappabar(Y) = ", len(kble)
    print "\talphabar(Y) = ", gds.equivalence.EnumAlphaBarClasses(q23, autq23)
    print ""


def NotEqual(a,b) :
    return a!=b

def HammingDistance(x,y) :
    assert len(x) == len(y)
    return sum( map(NotEqual, x, y) )

def HammingNorm(x) :
    return HammingDistance(x, len(x)*[gds.state.State(0, 2)] )


def main() :

    lacOperon = gds.biographs.LacOperon(0, 1, 1)

    g = lacOperon.GetGraph()
    f = lacOperon.GetFunctionList()
    n = nx.number_of_nodes(g)
    m = nx.number_of_edges(g)

    F = lacOperon.F
    F.SetParallel()
    F.SetBlockSequence([ [0,1,2,3,4,6,8,9], [5,7] ])
    lacOperon.SetParams(Ge = 0, Le = 0, Lem = 1)

#    transitions = gds.algorithms.GenerateTransitions(F)
#    print transitions
 
    p = gds.phase_space.PhaseSpace(F)
    T = p.GetTransitions()

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    print "fixed points:", fixedPoints
    print "periodicPoints:", periodicPoints
   

    n = F.GetDim();
    stateObjectList = F.stateObjectList
    limit = F.tupleConverter.limit
    ng = gds.util.enumeration.NTupleGenerator(limit)
    nStates = ng.Num()

    print n, nStates

    cNum = 0
    for cycle in periodicPoints :
        print "Cycle <%i>:" % cNum
        for xIndex in cycle :
            print "\t", F.tupleConverter.IndexToTuple( xIndex )
        cNum += 1


    sys.exit(0)

    x = n*[0]
    y = n*[0]
    image_x = n*[0]
    image_y = n*[0]

    diagram = []
    for i in range(0, n+1) :
        diagram.append( (n+1)*[0] )


    for i in xrange(0, nStates) :
        config = ng.Current()

        # Convert from index space to state space:
        for j in range(0,n) :
            x[j] = stateObjectList[j].IndexToState( config[j] )
        image_x =  F.tupleConverter.IndexToTuple( T[i] )

        ng2 = copy.deepcopy(ng)

#        print "x", x, image_x

        for j in xrange(i+1, nStates) :
            ng2.Next()
            config = ng2.Current()
            for k in range(0,n) :
                y[k] = stateObjectList[k].IndexToState( config[k] )

            hd = HammingDistance(x,y)
            image_y = ng.IndexToTuple( T[j] )
            hd2 = HammingDistance(image_x, image_y)
            diagram[hd][hd2] += 1
#            print x, y, image_x, image_y, hd, hd2

        ng.Next()



    print n, m



# ------------------------------------------------------------

if __name__ == "__main__":
    main()

#cProfile.run('main()', 'profile.txt')
