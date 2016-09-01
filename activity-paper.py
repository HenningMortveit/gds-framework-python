
import gds.util.enumeration
import gds.util
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
import networkx

def GenerateNetwork() :
    X = networkx.Graph()
    X.add_edge( 0, 1);
    X.add_edge( 0, 2);
    X.add_edge( 0, 3);
    X.add_edge( 0, 4);

    X.add_edge( 1, 9);
    X.add_edge( 2, 10);
    X.add_edge( 3, 11);
    X.add_edge( 4, 12);

    X.add_edge( 1, 6);    
    X.add_edge( 2, 7);    
    X.add_edge( 3, 8);    
    X.add_edge( 4, 5);    

    X.add_edge( 1, 5);    
    X.add_edge( 2, 6);    
    X.add_edge( 3, 7);    
    X.add_edge( 4, 8);    

    return X

def Construct(gds1) :
    """ """

    n = gds1.GetDim();
    stateObjectList = gds1.stateObjectList
    limit = gds1.tupleConverter.limit
    ng = gds.util.enumeration.NTupleGenerator(limit)
    nStates = ng.Num()

    x = n * [0]

    a0 = set()
    a1 = set()
    a2 = set()
    a3 = set()
    a4 = set()

    a1c = set()
    a2c = set()
    a3c = set()
    a4c = set()

    setCollection = [a0, a1, a2, a3, a4, a1c, a2c, a3c, a4c]

    for i in xrange(0, nStates) :

        config = ng.Current()
        ng.Next()

        # Convert from index space to state space:
        for j in range(0,n) :
            x[j] = stateObjectList[j].IndexToState( config[j] )

        if x[0].x != 0 :
            continue

        # Evaluate:
        y = gds1.Evaluate( x )
        x[0].x = 1
        z = gds1.Evaluate( x )

        for j in range(0, 5) :
            if y[j].x != z[j].x :
                setCollection[j].add(i)

        for j in range(5, 9) :
            if y[j-4].x == z[j-4].x :
                setCollection[j].add(i)
        
    for i in range(0,5) :
        print len(setCollection[i])

    print len( a0 | a1 | a2 | a3 | a4 )
    print len( a1 | a2 | a3 | a4 )
    print len( a0 & a1c & a2c & a3c & a4c )


def main() :

    G = GenerateNetwork() 
    n = networkx.number_of_nodes(G)
    k = 3

    stateObject = n * [gds.state.State(0, 2)]
    f = n * [gds.functions.threshold(k)]
    gds1 = gds.gds.GDS(G, f, stateObject)

    Construct(gds1)


main()

