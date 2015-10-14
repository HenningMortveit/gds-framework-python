# Algorithms on graphs.
#

import networkx

def CreateIndexMap(g) :
    """Creates the vertex indexed list of indices needed by vertex
    functions."""

    n = len(g.nodes())
    iMap = []

    #SW: It is assumed that a undirected graph has implicit self loop,
    #whereas a directed graph does not have unless the loop is
    #explicit.

    if not networkx.is_directed(g) :
        for i in range(0,n) :
	    n1 = g.neighbors(i)
            n1.append(i)
            n1.sort()
            iMap.append( n1 )
    else :
    	for i in range(0,n) :
	    n1 = g.predecessors(i)
            n1.sort()
            iMap.append( n1 )
    return iMap
