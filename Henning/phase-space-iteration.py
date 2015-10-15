 
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

import networkx as nx
import copy
import gds.biographs

def main() :

    lacOperon = gds.biographs.LacOperon(0, 0, 0)

    g = lacOperon.GetGraph()
    f = lacOperon.GetFunctionList()
    n = nx.number_of_nodes(g)
    m = nx.number_of_edges(g)

    F = lacOperon.F



    n = 4
    g = gds.graphs.CircleGraph(n)
    g.add_edge(0, 2);

    stateObject = n * [gds.state.State(0, 2)]
    f = n * [gds.functions.biThreshold(1,3)]

    F = gds.gds.GDS(g, f, stateObject, False)


#    gds1.SetSequence(pi)
    F.SetParallel()

    # We now have a gds object F.

#    transitions = gds.algorithms.GenerateTransitions(F)
#    print transitions
 
    p = gds.phase_space.PhaseSpace(F)

    print p.GetComponents()


    T = p.GetTransitions()

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    print fixedPoints
    print periodicPoints

    cNum = 0
    for cycle in periodicPoints :
        print "Cycle <%i>:" % cNum
        for xIndex in cycle :
            print "\t", F.tupleConverter.IndexToTuple( xIndex )
        cNum += 1
   
    n = F.GetDim();
    stateObjectList = F.stateObjectList
    limit = F.tupleConverter.limit
    ng = gds.util.enumeration.NTupleGenerator(limit)
    nStates = ng.Num()

    print n, nStates

    x = n*[0]
    image_x = n*[0]

    for i in xrange(0, nStates) :
        config = ng.Current() # The current tuple in index space

        # Convert from index space to state space. This is important:
        # in some cases like for dynamic threshold systems, vertex
        # states are tuples.

        for j in range(0,n) :
            x[j] = stateObjectList[j].IndexToState( config[j] )
        image_x =  F.tupleConverter.IndexToTuple( T[i] )
        print config, x, image_x
        
        ng.Next()

    print n, m


# ------------------------------------------------------------

if __name__ == "__main__":
    main()

#cProfile.run('main()', 'profile.txt')
