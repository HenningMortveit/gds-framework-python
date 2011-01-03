#
# Algorithms on graphs.
#

import networkx

def CreateIndexMap(g) :
    """Creates the vertex indexed list of indices needed by vertex
    functions."""

    n = len(g.nodes())
    iMap = []
    for i in range(0,n) :
        n1 = g.neighbors(i)
        n1.append(i)
        n1.sort()
        iMap.append( n1 )
    return iMap
