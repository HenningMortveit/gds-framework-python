#
#
#

import state
import graphs
import functions
import gds
import util.enumeration

def FixedPoints( gds, transitions = None ) :
    fixedPoints = []
    if transitions == None :
        transitions = GenerateTransitions(gds)
    for x, y in enumerate(transitions ) :
        if x == y :
            fixedPoints.append(x)
    return fixedPoints

def PeriodicPoints( gds, transitions = None ) :
    pass

def GenerateTransitions(gds) :
    """ """

    n = gds.GetDim();
    stateObjectList = gds.stateObjectList
    limit = gds.tupleConverter.limit
    ng = util.enumeration.NTupleGenerator(limit)
    nStates = ng.Num()

    x = n * [0]
    z = n * [0]

    M = nStates * [-1]

    for i in xrange(0, nStates) :
        config = ng.Current()

        # Convert from index space to state space:
        for j in range(0,n) :
            x[j] = stateObjectList[j].IndexToState( config[j] )

        # Evaluate:
        y = gds.Evaluate( x )

        # Convert from state space to index space:
        for j in range(0,n) :
            z[j] = stateObjectList[j].StateToIndex( y[j] )

        # Compute index from index tuple:
        k = ng.TupleToIndex( z )

        M[i] = k

        #print i, config, x, "->", y, z, k

        ng.Next()

    return M
