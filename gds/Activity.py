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
# 8. number of acyclic orientations
################################################################################

### ----------------------------------------------------------------------------
### Modification history
### Dec. 27 2013
### Fix the subgraph label problem, subgraph nodes now have their own label
### following 0,1,2...

### Jan. 09 2014
### Add the module to compute the number of acyclic orientations

### Jan. 27 2014
### Make changes to accomodate directed graphs
### ----------------------------------------------------------------------------

import os
import sys
import math
import gds
import copy
import algorithms
import graphs
import networkx
import equivalence
import matplotlib.pyplot as plt
from biographs import *

class Activity :
    def __init__(self, g, f, iNode, iMap=None) :
        self.graph = g
        self.iNode = iNode
        #self.n1 = list()
        #self.n2 = list()
        self.func = copy.deepcopy(f)
        self.iMap = copy.deepcopy(iMap)
        self.sgIMap = None
        self.labelMap = dict()
        self.reverseLabelMap = dict()
        if networkx.is_directed(g) :
            self.SetDiSubgraph()
            #self.SetGraph()
        else :
            self.SetSubgraph()
            #self.SetGraph()
        self.SetGDS()
        self.activity = 0
        self.diff = 0

    def SetGraph(self) :
        self.sg = self.graph

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
        self.subNodes = list(set(self.subNodes)) #eliminate duplicated nodes resulted from loop
        self.subgraph = self.graph.subgraph(self.subNodes)

        #relabel the subgraph nodes, follow the consecutive order: 0, 1, 2.....
        #subgraph keeps the node label from the original graph, sg keeps its own node label
        l = 0
        for node in self.subNodes :
            self.labelMap[node] = l
            self.reverseLabelMap[l] = node
            l = l + 1
        self.sg = networkx.Graph(networkx.relabel_nodes(self.subgraph,self.labelMap))
        self.close_sgn1 = list() #closed d1 neighbors in sg
        for node in self.n1 :
          self.close_sgn1.append(self.labelMap[node])
        self.close_sgn1.append(self.labelMap[self.iNode])
        self.iNode = self.labelMap[self.iNode]
    
    def SetDiSubgraph(self) :
        """Directed version of Setsubgraph
	    Extract the distance-2 subgraph X(i;2)"""
        self.n1 = self.graph.neighbors(self.iNode) + self.graph.predecessors(self.iNode)
        self.n2 = list()
        for node in self.n1 :
            neighbor = self.graph.neighbors(node) + self.graph.predecessors(node)
            for n in neighbor :
                if (not self.graph.has_edge(n, self.iNode) and n != self.iNode) :
                    self.n2.append(n)
        #Delete the duplicated nodes
        self.n2 = list(set(self.n2))

        self.d1 = len(self.n1)
        self.d2 = len(self.n2)
        self.subNodes = [self.iNode]
        self.subNodes = self.subNodes + self.n1 + self.n2
        self.subNodes = list(set(self.subNodes)) #eliminate duplicated nodes resulted from loop
        self.subgraph = self.graph.subgraph(self.subNodes)

        #relabel the subgraph nodes, follow the consecutive order: 0, 1, 2.....
        #subgraph keeps the node label from the original graph, sg keeps its own node label
        l = 0
        for node in self.subNodes :
            self.labelMap[node] = l
            self.reverseLabelMap[l] = node
            l = l + 1
        self.sg = networkx.Graph(networkx.relabel_nodes(self.subgraph,self.labelMap))
        self.close_sgn1 = list() #closed d1 neighbors in sg
        for node in self.n1 :
          self.close_sgn1.append(self.labelMap[node])
        self.close_sgn1.append(self.labelMap[self.iNode])
        self.iNode = self.labelMap[self.iNode]

    def SetGDS(self) :
	"""Set up the GDS of X(i;2)"""
        n = len(self.sg.nodes())
        if self.iMap != None : #reset iMap such that it only contains the nodes in the subgraph
            self.sgIMap = dict()
            for node in self.graph.nodes():
                if not self.subgraph.has_node(node) : #remove the node not in the subgraph from iMap
                    self.iMap.pop(node)
            for node in self.iMap : #remove neighbors not in the subgraph for each node in iMap
                newNeighborList = list()
                for neighbor in self.iMap[node] :
                    if self.subgraph.has_node(neighbor) :
                        newNeighborList.append(neighbor)
                self.iMap[node] = newNeighborList

            for node in self.iMap : #maping the indices from the original graph to the subgraph for iMap
                sgNode = self.labelMap[node]
                sgNeighbors = list()
                for neighbor in self.iMap[node] :
                    sgNeighbors.append(self.labelMap[neighbor])
                self.sgIMap[sgNode] = sgNeighbors
       
        if isinstance(self.func,list) : #non-uniform functions
            function = list()
            for i in range(n):
                function.append(self.func[self.reverseLabelMap[i]]) #find the corresponding vertex function from the original function list
        else:  #uniform founctions
            function = n * [self.func]
        
    	stateObject = n * [gds.state.State(0, 2)]
        self.gds = gds.GDS(self.sg, function, stateObject, False, self.sgIMap)
        pi = [self.close_sgn1]
        self.gds.SetBlockSequence(pi) #only evaluate nodes in closed d1 neighborhood

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

    def GetAcyclicOrientationsNumber(self) :
        acyc, le = equivalence.AcyclicOrientations(self.sg)
	self.acycNumber = len(acyc)
        return self.acycNumber

