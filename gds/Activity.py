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

### ----------------------------------------------------------------------------
### Modification history
### Dec. 27 2013
### Fix the subgraph label problem, subgraph nodes now have their own label
### following 0,1,2...
### ----------------------------------------------------------------------------

import os
import sys
import math
import gds
import algorithms
import graphs
import networkx
import matplotlib.pyplot as plt

class Activity :
    def __init__(self, g, f, iNode) :
        self.graph = g
        self.iNode = iNode
        self.func = f
        self.SetSubgraph()
        self.SetGDS()
        self.activity = 0
        self.diff = 0

    def SetSubgraph(self) :
	"""Extract the distance-2 subgraph X(i;2)"""
        self.n1 = self.graph.neighbors(self.iNode)
        self.n2 = list()
        for node in self.n1 :
            neighbor = self.graph.neighbors(node)
            for n in neighbor :
                if (not self.graph.has_edge(n, self.iNode) and n != self.iNode) :
                    self.n2.append(n)
        #Delete the duplicated nodes
        self.n2 = list(set(self.n2))

        self.d1 = len(self.n1)
        self.d2 = len(self.n2)
        self.subNodes = [self.iNode]
        self.subNodes = self.subNodes + self.n1 + self.n2
        self.subgraph = self.graph.subgraph(self.subNodes)

        #relabel the subgraph nodes, follow the consecutive order: 0, 1, 2.....
        #subgraph keeps the node label from the original graph, sg keeps its own node label
        labelMap = dict()
        l = 0
        for node in self.subNodes :
            labelMap[node] = l
            l = l + 1
        self.sg = networkx.Graph(networkx.relabel_nodes(self.subgraph,labelMap))
        self.iNode = 0
    
        print self.sg.nodes()
        print self.subNodes

    def SetGDS(self) :
	"""Set up the GDS of X(i;2)"""
        n = len(self.sg.nodes())
        function = n * [self.func]
    	stateObject = n * [gds.state.State(0, 2)]
    	self.gds = gds.GDS(self.sg, function, stateObject, False)

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

    def GetSubgraph (self) :
        return self.subgraph

    def GetActivity (self): 
        return self.activity

    def GetDiff (self) :
        return self.diff

    def GetD1(self) :
        """Get the degree of node i"""
        return self.d1

    def GetD2(self) :
        """Get the number of distance-2 nodes of node i"""
        return self.d2 

    def GetT3(self) :
        """Get type 3 edge number"""
        self.t3 = 0
        for i in range(0, len(self.n1)-1) :
            for j in range(i+1, len(self.n1)) :
                if (self.subgraph.has_edge(self.n1[i],self.n1[j])) :
                    self.t3 = self.t3 + 1
        return self.t3

    def GetT4(self) :
        self.t4 = 0
        for i in range(0, len(self.n1)) :
            for j in range(0, len(self.n2)):
                if (self.subgraph.has_edge(self.n1[i],self.n2[j])) :
                    self.t4 = self.t4 + 1
        #Exclude the original edges
        self.t4 = self.t4 - self.d2
        return self.t4

    def GetChromaticNumber(self) :
        "Compute the chromatic number of X(i;2)"
        #Based on greedy algorithm, can be arbitrary bad due to the ordering of the vertices.
        ncolor = 1
        while(True) :
            if (self.CanColor(ncolor)) :
                self.chromaticNumber = ncolor
                return self.chromaticNumber
            else :
                ncolor = ncolor + 1

    def CanColor(self,ncolor) :
        #colorMap<v,c>, where v is the vertex, c is the color assigned to it.
        colorMap = {}
        for node in self.sg.nodes() :
            colorMap[node] = 0
        for node in self.sg.nodes() :
            colorAvail = range(1, ncolor + 1)
            for neighbor in self.sg.neighbors(node) :
                if (colorMap[neighbor] != 0 and colorMap[neighbor] in colorAvail) :
                    colorAvail.remove(colorMap[neighbor])
            if (len(colorAvail) != 0) :
                colorMap[node] = colorAvail[0]
            else :
                return False
        return True

    
def main() :
    #-----------------------------------
    X = networkx.gnp_random_graph(20, 0.2)
    networkx.draw(X)
    plt.savefig("./graphs/gnp-20-0.3.png")
    plt.clf()
    result = open("Activity-gnp-20-0.3.csv", 'w')
    result.write("#node_i \t activity \t d(i) \t d2(i) \t t3(i) \t t4(i) \t \chi(i) \n")
    for node in X.nodes() :
        f = gds.functions.threshold(3)
        A = Activity(X, f, node)
        A.ComputeActivity()
        print A.GetT4()
        result.write("%d \t %f \t %d \t %d \t %d \t %d \t %d \n"%(node, A.GetActivity(), A.GetD1(), A.GetD2(), A.GetT3(), A.GetT4(), A.GetChromaticNumber()))
	networkx.draw(A.GetSubgraph())
	plt.savefig("./graphs/subgraph-%d" %node)
	plt.clf()
    result.close()




    sys.exit(0)

    #----------------------------------
    X = networkx.Graph()
    edges = [
         [0,1],[0,2],[0,3],
         [1,4],[1,5],
         [2,6],[2,7],
         [3,8],[3,9]
         ]
    for e in edges :
        X.add_edge(e[0], e[1])
    X.add_edge(1,3)
    #X.add_edge(1,6)
    #X.add_edge(3,7)
    #X.add_edge(6,7)
    #X.add_edge(9,10)
    #X.add_edge(10,11)
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
    #X.add_edge(0,3)
    #X.add_edge(3,1)
    #X.add_edge(1,2)
    #X.add_edge(3,0)
    #X.add_edge(1,3)
    #X = networkx.gnp_random_graph(10, 0.25)
    #X.add_node(0)
    #networkx.draw(X)
    plt.savefig("X.png")

    f = gds.functions.threshold(1)

    A = Activity(X, f, 0)
    A.ComputeActivity()
    print "Chromatic number:",A.GetChromaticNumber()
    print "Diff:", A.GetDiff()
    
if __name__ == "__main__" :
    main()
