import sys

# modify to your dir
# sys.path += ['C:/Users/vgncsmallssd/Desktop/gds-framework-python-master/gds-framework-python-master/gds/']

# from /gds/
import gds.biographs
import gds.phase_space
import gds.graphs
import gds.functions
import gds.state
import gds.gds
import gds.algorithms
import gds.equivalence
import gds.util.enumeration
from collections import Counter

def get_system_multiset(bio_system):

    # Retrieve dependency graph G
    G = bio_system.GetGraph()

    # Remove self-loops and replace directed edges with undirected edges
    n = G.selfloop_edges()
    G.remove_edges_from(n)
    G = G.to_undirected()

    (Acyc_G, linExt) = gds.equivalence.AcyclicOrientations(G)

    print "alpha(G) =", len(Acyc_G)  # No. of Acyclic orientations

    # Get [Kappa Classes composed of Acyc_G]
    kappa_G = gds.equivalence.EnumKappaClasses(G)  # No. of Kappa classes

    print "kappa(G) =", kappa_G

    # get [Kappa Class representatives]
    Acyc_G_kappa_reps = gds.equivalence.KappaLinearExtensions(G, 0)  # Vertex 0 is maximal degree

    F = bio_system.F

    fixedPoints = []

    freq_multi_set = {}

    for rep in Acyc_G_kappa_reps:

        multi_set = []
        F.SetSequence(rep)
        p = gds.phase_space.PhaseSpace(F)
        periodicPoints = p.GetPeriodicPoints()

        cNum = 0
        for cycle in periodicPoints:
            multi_set.append(len(cycle))
            ''' # display periodic points
            print "Cycle <%i>:" % cNum
            for xIndex in cycle:
                print "\t", F.tupleConverter.IndexToTuple(xIndex)
            '''
            cNum += 1

        if rep == Acyc_G_kappa_reps[-1]:
            fixedPoints = p.GetFixedPoints() # Fixed Pts. invariant under sequential update
            fixedPoints = [F.tupleConverter.IndexToTuple(i) for i in fixedPoints]

        multi_set.sort()
        multi_set_key = tuple(multi_set)
        if multi_set_key in freq_multi_set:
            freq_multi_set[multi_set_key] += 1
        else:
            freq_multi_set[multi_set_key] = 1


    print "cycle multiset frequencies: ", freq_multi_set
    print "fixed points: ", fixedPoints

def main():
    # system analysis
    print "Lac Operon Example"

    lacOperon = gds.biographs.LacOperon(Ge=0, Le=0, Lem=1)
    get_system_multiset(lacOperon)

    sys.exit(0)

    # Lac Operon graph measures
    lacOperon = gds.biographs.LacOperon(Ge=1, Le=0, Lem=0)
    G = lacOperon.GetGraph()

    # Remove self-loops and replace directed edges with undirected edges
    n = G.selfloop_edges()
    G.remove_edges_from(n)
    G = G.to_undirected()


    (Acyc_G, linExt) = gds.equivalence.AcyclicOrientations(G)

    print "alpha(G) =", len(Acyc_G)  # No. of Acyclic orientations

    # Get [Kappa Classes composed of Acyc_G]
    kappa_G = gds.equivalence.EnumKappaClasses(G)  # No. of Kappa classes

    print "kappa(G) =", kappa_G

    # get [Kappa Class representatives]
    Acyc_G_kappa_reps = gds.equivalence.KappaLinearExtensions(G, 0)  # Vertex 0 is maximal degree

    print Acyc_G_kappa_reps



    sys.exit(0)




# ------------------------------------------------------------
if __name__ == "__main__":
    main()
