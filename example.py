

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

import networkx as nx
from networkx.algorithms import *

import copy
import sys
import cProfile


def SDSExample() :
    """Basic example for phase space on X = Circle_4."""

    n = 4
    pi = [0, 2, 1, 3]
    circ = gds.graphs.CircleGraph(n)
    #f = n * [gds.functions.wolfram(150)]
    f = n * [gds.functions.nor]
    stateObject = n * [gds.state.State(0, 2)]

    gds1 = gds.gds.GDS(circ, f, stateObject, True)
    gds1.SetSequence(pi)

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

    return transitions




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


def main() :

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


# ------------------------------------------------------------


main()

#cProfile.run('main()', 'profile.txt')
