#

import networkx as nx
import matplotlib.pyplot as plt

def biograph () :
    X = nx.DiGraph()
    edges = [("EMF1","EMF1",{"weight":1}), ("EMF1","TFL1",{"weight":1}),
	     ("EMF1","LFY",{"weight":-2}), ("EMF1","AP1",{"weight":-1}),
	     ("TFL1","LFY",{"weight":-1}), ("TFL1","AG",{"weight":-2}),
	     ("LFY","TFL1",{"weight":-2}),  ("LFY","AP1",{"weight":-5}), 
	     ("LFY","CAL",{"weight":2}),  ("LFY","AG",{"weight":1}), 
	     ("LFY","AP3",{"weight":3}),  ("LFY","PI",{"weight":4}), 
             ("AP1","LFY",{"weight":2}), ("AP1","AG",{"weight":-2}),
	     ("CAL","LFY",{"weight":1}),
	     ("LUG","AG",{"weight":-1}),
	     ("UFO","AP3",{"weight":2}), ("UFO","PI",{"weight":1}),
	     ("BFU","AP3",{"weight":1}), ("BFU","PI",{"weight":1}),
	     ("AG","AP1",{"weight":-1}),
	     ("AP3","BFU",{"weight":1}),
	     ("PI","BFU",{"weight":1}),
	     ("SUP","AP3",{"weight":-2}), ("SUP","AP3",{"weight":-1}),
            ]
    X.add_edges_from(edges)

    labelMap = {"EMF1" : 0, "TFL1" : 1, "LFY" : 2, "AP1" : 3,
                "CAL" : 4, "LUG" : 5, "UFO" : 6, "BFU" : 7,
                "AG" : 8, "AP3" : 9, "PI" : 10, "SUP" : 11
               }
    G = nx.DiGraph(nx.relabel_nodes(X,labelMap))   
    print labelMap
    return G


def main() :
    X= biograph()
    #nx.draw(X, pos = nx.spring_layout(X))
    #plt.show()

if __name__ == "__main__" :
    main() 
