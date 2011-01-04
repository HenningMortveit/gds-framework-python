

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



transitions = SDSExample()


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


NetworkXExample(transitions)

#import itertools

#for p in itertools.chain(itertools.permutations([0,1,2,3])) :
#    print p

def OrientationExample() :
    circ =  gds.graphs.CircleGraph(4)
    pi = gds.sequence.Permutation([0,1,2,3])
    aO = gds.orientation.Orientation(circ, pi = pi)

    print "Orientation", "{3,2}", aO( (3,2) )

    print "Orientation:", aO
    print "Linear extension: ", aO.LinearExtension()

OrientationExample()



circ = gds.graphs.PathGraph(6)
circ = gds.graphs.WheelGraph(4)
circ = gds.graphs.HyperCube(dim = 3, base = 2)
circ = gds.graphs.CircleGraph(4)

print circ.nodes()
print circ.edges()

print "Linear extensions"
le = gds.equivalence.LinearExtensions( circ )
#print le

print "Kappa linear extensions"
kle = gds.equivalence.KappaLinearExtensions(circ, 0)

#print kle

print "alpha(Y) = ", len(le)
print "kappa(Y) = ", len(kle)


kappaEqClasses = gds.equivalence.KappaClasses(circ)
for i, eqClass in enumerate(kappaEqClasses) :
    print "Class:", i
    for p in eqClass :
        print "\t", p[1]

circ = gds.graphs.HyperCube(dim = 3, base = 2)
print "alpha(Y) = ", gds.equivalence.EnumAcyclicOrientations(circ)


c4 = gds.groups.C_n( 4 )
print len(c4), c4
d4 = gds.groups.D_n( 4 )
print len(d4), d4

aq23 = gds.groups.CreateAutQ2_3()
print len(aq23), aq23
