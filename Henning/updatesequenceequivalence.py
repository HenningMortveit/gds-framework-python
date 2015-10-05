 
#import pygraphviz as pgv

import sys
sys.path += ["/Users/henning/git/gds"]

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


def main() :

    lacOperon = gds.biographs.LacOperon(0, 0, 0)

    g = lacOperon.GetGraph()
    f = lacOperon.GetFunctionList()
    n = g.size()

    print g
    print f
    print n

    stateObject = n * [gds.state.State(0, 2)]

    gds1 = gds.gds.GDS(g, f, stateObject, False)

    print gds1

    return

    le = gds.equivalence.LinearExtensions( lacOperon.GetGraph() )

    s = list()

    for pi in le :
        gds1.SetSequence(pi)
        transitions = gds.algorithms.GenerateTransitions(gds1)
        if not transitions in s :
            s.append(transitions)

    print len(s)
#    p = gds.phase_space.PhaseSpace(gds1)




    sys.exit(0)

    UpdateSequenceEquivalenceExample()


# ------------------------------------------------------------

if __name__ == "__main__":
    main()

#cProfile.run('main()', 'profile.txt')
