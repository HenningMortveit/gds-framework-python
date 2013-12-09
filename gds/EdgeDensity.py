import os
import math
import gds
import algorithms
import graphs
import networkx

class EdgeDensity :
    def  __init__(self, g, f, iNode, type3Edge, type4Edge):
        self.SetSubgraph(g, iNode, type3Edge, type4Edge)
        self.SetGDS(f)
        self.diff = 0
        self.activity = 0
     
    def SetSubgraph (self, g, iNode, type3Edge, type4Edge) :
	"""Form the subgraph associated with node i and its distance-1 and distance-2 neighbors.
           Add type-3 and type-4 edges into that subgraph.          
        """
        self.graph = g
        self.iNode = iNode
        self.type3Edge = type3Edge
        self.type4Edge = type4Edge
        n1 = self.graph.neighbors(self.iNode)
        n2 = list()
        for node in n1 :
            neighbor = self.graph.neighbors(node)
            for n in neighbor :
                if (n !=node and n != iNode) :
                    n2.append(n)
        #Delete the duplicated nodes
        n2 = list(set(n2))

        subNodes = list()
        subNodes = (n1+n2)
        subNodes.append(iNode)
        self.subgraph = self.graph.subgraph(subNodes)

        #Add type3 edges
        type3 = self.type3Edge
        for i in range(0, len(n1)) :
            for j in range (i+1, len(n1)) :
                if (type3 > 0 and not self.subgraph.has_edge(n1[i],n1[j])) :
                    self.subgraph.add_edge(n1[i],n1[j])
                    type3 = type3 - 1
                    print "Type 3 edge (%d, %d) added" %(n1[i],n1[j])
                elif (type3 == 0) :
                    break
        if (type3 > 0):
            print "ERROR: Cannot add that much type3 edges! %d added" %(self.type3Edge - type3)
     
        #add type4 edges
        type4 = self.type4Edge
        for i in range(0, len(n1)) :
            for j in range (0, len(n2)) :
                if (type4 > 0 and not self.subgraph.has_edge(n1[i],n2[j])) :
                    self.subgraph.add_edge(n1[i],n2[j])
                    type4 = type4 - 1
                    print "Type 4 edge (%d, %d) added" %(n1[i],n2[j])
                elif (type4 == 0) :
                    break
        if (type4 > 0):
            print "ERROR: Cannot add that much type4 edges! %d added" %(self.type4Edge - type4)
        print "Subgraph nodes:", self.subgraph.nodes()


    def SetGDS(self, f) :
        n = len(self.subgraph.nodes())
        function = n * [f]
    	stateObject = n * [gds.state.State(0, 2)]
   	self.gds = gds.GDS(self.subgraph, function, stateObject, False)
  

    def ComputeActivity(self):
        """Compute alpha_{F,i}"""
   	transitions = algorithms.GenerateTransitions(self.gds)

    	for x,y in enumerate(transitions) :
        	state = self.gds.IntegerToState(x)
        	iFlipState = state
        	if (iFlipState[self.iNode].x == 0) :
            		iFlipState[self.iNode].x = 1
        	else :
            		iFlipState[self.iNode].x = 0
        	iFlipStateIndex = self.gds.StateToInteger(iFlipState)
        	iFlipImageIndex = transitions[iFlipStateIndex]
        	if (y != iFlipImageIndex) :
            		self.diff = self.diff + 1
    	self.activity = float(self.diff)/(2**self.gds.GetDim())
    	print "different image:", self.diff
    	print self.activity
 
    def GetActivity (self): 
        return self.activity

def main() :
    X = networkx.Graph()
    edges = [
         [0,1],[0,2],[0,3],
         [1,4],[1,5],
         [2,6],[2,7],
         [3,8],[3,9]
         ]
    for e in edges :
        X.add_edge(e[0], e[1])
    X.add_edge(9,10)
    X.add_edge(10,11)
    f = gds.functions.threshold(1)
    
    type3 = range(4)
    type4 = range(13)
    for i in range(0, len(type4)) :
        for j in range(0, len(type3)) :
            print "_____________________type 3: %d  type 4: %d___________________________\n" %(type3[j],type4[i])
            D = EdgeDensity(X, f, 0, type3[j], type4[i])
            D.ComputeActivity()

    

if __name__ == "__main__" :
    main()
