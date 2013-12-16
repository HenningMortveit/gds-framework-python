import os
import sys
import math
import gds
import algorithms
import graphs
import networkx
import random
import numpy

class EdgeDensity :
    def  __init__(self, g, f, iNode, type3Edge, type4Edge):
        self.SetSubgraph(g, iNode, type3Edge, type4Edge)
        self.SetGDS(f)
        self.diff = 0
        self.activity = 0
     
    def SetSubgraph (self, g, iNode, type3Edge, type4Edge) :
	"""1. Form the subgraph associated with node i and its distance-1 and distance-2 neighbors.
       2. Generate the possible type3 and type4 edge list. 
       3. Randomly add edges into the subgraph from the list.
       Naming:
       type3Edge: the number of type3 edges to add
       type3EdgeList: the list of possible type3 edges that can be added
       edge3: the list of type3 edges that are selected from type3EdgeList to add.
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
        
        #Generate the possible type3 edge and type4 edge lists
        self.type3EdgeList = list()
        self.type4EdgeList = list()
        
        for i in range(0, len(n1)) :
            for j in range(i+1, len(n1)) :
                if (not self.subgraph.has_edge(n1[i], n1[j])) :
                    self.type3EdgeList.append([n1[i], n1[j]])

        for i in range(0, len(n1)) :
            for j in range(0, len(n2)) :
                if (not self.subgraph.has_edge(n1[i],n2[j])) :
                    self.type4EdgeList.append([n1[i],n2[j]])
        
        #---------------------------------------------------------------
        #Randomly add edges into the subgraph, using Reservoir Sampling Algorithm.
        self.edge3 = list()
        self.edge4 = list()
        if (self.type3Edge > len(self.type3EdgeList)) :
            print "ERROR: Exceed the type3 edges upper bound %d!" %len(self.type3EdgeList)
            sys.exit(0)
        if (self.type4Edge > len(self.type4EdgeList)) :
            print "ERROR: Exceed the type4 edges upper bound %d!" %len(self.type4EdgeList)
            sys.exit(0)
        if (self.type3Edge != 0) :
            for i in range(0, self.type3Edge) :
                self.edge3.append(self.type3EdgeList[i])
            for i in range(self.type3Edge, len(self.type3EdgeList)) :
                j = random.randint(0, i)
                if (j < self.type3Edge):
                    self.edge3[j] = self.type3EdgeList[i]

        if (self.type4Edge != 0) :
            for i in range(0, self.type4Edge) :
                self.edge4.append(self.type4EdgeList[i])
            for i in range(self.type4Edge, len(self.type4EdgeList)) :
                j = random.randint(0, i)
                if (j < self.type4Edge):
                    self.edge4[j] = self.type4EdgeList[i]
        
        for e in self.edge3 :
            self.subgraph.add_edge(e[0], e[1])
        for e in self.edge4 :
            self.subgraph.add_edge(e[0], e[1])

        #Add type3 edges
        #type3 = self.type3Edge
        #for i in range(0, len(n1)) :
        #    for j in range (i+1, len(n1)) :
        #        if (type3 > 0 and not self.subgraph.has_edge(n1[i],n1[j])) :
        #            self.subgraph.add_edge(n1[i],n1[j])
        #            type3 = type3 - 1
        #            #print "Type 3 edge (%d, %d) added" %(n1[i],n1[j])
        #        elif (type3 == 0) :
        #            break
        #if (type3 > 0):
        #    print "ERROR: Cannot add that much type3 edges! %d added" %(self.type3Edge - type3)
     
        #add type4 edges
        #type4 = self.type4Edge
        #for i in range(0, len(n1)) :
        #    for j in range (0, len(n2)) :
        #        if (type4 > 0 and not self.subgraph.has_edge(n1[i],n2[j])) :
        #            self.subgraph.add_edge(n1[i],n2[j])
        #            type4 = type4 - 1
        #            #print "Type 4 edge (%d, %d) added" %(n1[i],n2[j])
        #        elif (type4 == 0) :
        #            break
        #if (type4 > 0):
        #    print "ERROR: Cannot add that much type4 edges! %d added" %(self.type4Edge - type4)
        #print "Subgraph nodes:", self.subgraph.nodes()


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
