################################################################################
# SW
# Dec. 18 2013
# Given the graph,system function and node i, this code computes following values
# associated with node i:
# 1. activity: \alpha{F,i}
# 2. degree: d(i)
# 3. number of distance-2 neighbors: d2(i)
# 4. number of type-3 edges: t3(i)
# 5. number of type-4 edges: t4(i)
# 6. distance-2 subgraph of node i: X(i;2)
# 7. chromatic number of X(i;2): \chi(i) 
################################################################################

import os
import sys
import math
import gds
import algorithms
import graphs
import networkx

class Activity :
    def __init__(self, g, f, iNode) :
        self.graph = g
        self.iNode = iNode
	self.func = f
        self.SetSubgraph()
        self.SetGDS(f)
        self.activity = 0
	self.diff = 0

    def SetSubgraph(self) :
	"""Extract the distance-2 subgraph X(i;2)"""
        self.n1 = self.graph.neighbors(self.iNode)
        self.n2 = list()
        for node in self.n1 :
            neighbor = self.graph.neighbors(node)
            for n in neighbor :
                if (n !=node and n != self.iNode) :
                    self.n2.append(n)
        #Delete the duplicated nodes
        self.n2 = list(set(self.n2))

        self.subNodes = list()
        self.subNodes = (self.n1+self.n2)
        self.subNodes.append(self.iNode)
        self.subgraph = self.graph.subgraph(self.subNodes)

    def SetGDS(self) :
	"""Set up the GDS of X(i;2)"""
        n = len(self.subgraph.nodes())
        function = n * [self.func]
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
    	#print "different image:", self.diff
    	#print self.activity

    def GetActivity (self): 
        return self.activity

    def GetDiff (self) :
        return self.diff

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
    #edges = [
    #    [0,1],[0,2],[0,3],[0,4],
    #    [1,5],[1,6],[1,7],
    #    [2,8],[2,9],[2,10],
    #    [3,11],[3,12],[3,13],
    #    [4,14],[4,15],[4,16]
    #        ]
    #for e in edges :
    #    X.add_edge(e[0], e[1])
    #X.add_edge(16,17)
    f = gds.functions.threshold(3)
    
    sampleSize = 5 #compute activity several times and take average
    type3 = range(4)
    type4 = range(13)
    print "#T4\T3 \t 0 \t 1 \t 2 \t 3"
    for i in range(0, len(type4)) :
        s = "%d \t" %i
        for j in range(0, len(type3)) :
            sumActivity = 0
            activityList = list()
            for k in range(0, sampleSize) :
                D = EdgeDensity(X, f, 0, type3[j], type4[i])
                D.ComputeActivity()
                #activityList.append(D.GetActivity())
                sumActivity = sumActivity + D.GetActivity()
            s = s + "%f\t" %(sumActivity/sampleSize)
            #s = s + "%f\t" %(numpy.std(activityList, axis = 0))
        print s 

    #D = EdgeDensity(X, f, 0, 3, 5)
    #D.ComputeActivity()
    #print D.GetActivity()
    
if __name__ == "__main__" :
    main()
