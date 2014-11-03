################################################################################
# Feb. 4 2014
# This module stores a set of biology networks. A network object has a graph, 
# a list of functions, and information such as bibtex reference,
# name, domain("biology" for this module), etc.
################################################################################

import networkx as nx
import matplotlib.pyplot as plt
import state
import Activity
import functions

class MendozaAlvarezBuylla() :
    
    def __init__(self) :
        self.bibtex = """@article{demongeot2010attraction,
  			title={Attraction basins as gauges of robustness against boundary conditions in biological complex systems},
  			author={Demongeot, Jacques and Goles, Eric and Morvan, Michel and Noual, Mathilde and Sen{\'e}, Sylvain},
  			journal={PloS one},
  			volume={5},
  			number={8},
  			pages={e11793},
  			year={2010},
  			publisher={Public Library of Science}
			}
			"""
	self.name = "MendozaAlvarezBuylla"
        self.description = "Original Mendoza & Alvarez-Buylla Network"
        self.domain = "biology"
        self.g = self.CreateGraph()
        self.f = self.SetFunctionList()

    def CreateGraph(self) :
    	X = nx.DiGraph()
    	edges = [("EMF1","EMF1",{"weight":1}), ("EMF1","TFL1",{"weight":1}),
	     	("EMF1","LFY",{"weight":-2}), ("EMF1","AP1",{"weight":-1}),
	     	("TFL1","LFY",{"weight":-1}), ("TFL1","AG",{"weight":-2}),
	     	("LFY","TFL1",{"weight":-2}),  ("LFY","AP1",{"weight":5}), 
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
	     	("SUP","AP3",{"weight":-2}), ("SUP","PI",{"weight":-1}),
            	]
    	X.add_edges_from(edges)

    	self.labelMap = {"EMF1" : 0, "TFL1" : 1, "LFY" : 2, "AP1" : 3,
                "CAL" : 4, "LUG" : 5, "UFO" : 6, "BFU" : 7,
                "AG" : 8, "AP3" : 9, "PI" : 10, "SUP" : 11
               	}
    	return nx.DiGraph(nx.relabel_nodes(X,self.labelMap))  
 
    def SetFunctionList(self) :
	threshold = [0, 0, 3, -1, 1, 0, 0, 1, -1, 0, 0, 0]
	f = list()
        #for t in threshold :
	#    f.append(generalizedThreshold(t))
	for node in self.g.nodes():
	#    f.append(functions.threshold(1))
	#    f.append(functions.indicator(4))
	    f.append(functions.nor)
	return f

    
    def GetGraph(self) :
	return self.g
	
    def GetFunctionList(self) :
	return self.f
	
    def GetBibtex(self) :
	return self.bibtex
	
    def GetName(self) :
	return self.name
    
    def GetDomain(self) :
	return self.domain




class I5GroupTTSS() :

    def __init__(self) :
    	self.bibtex = """@article{MacLean2010Boolean,
        title = { A Boolean Model of the Pseudomonas syringae hrp Regulon Predicts a Tightly Regulated System} ,
        author = {MacLean, Daniel and Studholme , David J.} ,
        journal = {PloS one},
        volume = {5},
        number = {2},
        pages = {e9101},
        year = {2010},
        publisher = {Public Library of Science}
        }
        """
	self.name = "I5GroupTTSS"
    	self.description = " Pseudomonas syringae of I[5] group "
    	self.domain = "biology"
    	self.g = self.CreateGraph()
    	self.f = self.SetFunctionList()

    def CreateGraph(self) :
    	Y = nx.DiGraph()
    	edgeSet = [("gacSgacA" , "hrpRS", {"weight":1}) , ("gacSgacA" , "rponN", {"weight":1}) ,
               ("hrpRS" , "hrpL", {"weight":1}) , ("rponN" , "hrpV" , {"weight":1}) ,
               ("rponN" , "hrpL", {"weight":1}) , ("hrpL" , "hrpV", {"weight":1}) ,
               ("hrpL" , "hrpG", {"weight":1}) , ("hrpL" , "hrpA" , {"weight":1}) ,
               ("hrpA" , "hrpRS" , {"weight":2}) , ("hrpV" , "hrpRS", {"weight": -1}) ,
               ("hrpG" , "hrpV" , {"weight": -1})
               ]
        
    	Y.add_edges_from(edgeSet)
            
    	self.labelMap = {"gacSgacA" : 0 , "hrpRS" : 1 , "rponN" : 2 , "hrpV" : 3 , "hrpL" : 4 , "hrpG" : 5 , "hrpA" : 6 }
            
    	return nx.DiGraph(nx.relabel_nodes(Y,self.labelMap))
            
    def SetFunctionList(self) :
		f = list()
		#f = [self.f0, self.f1, self.f2, self.f3, self.f4, self.f5, self.f6]
		for node in self.g.nodes():
	    	#    f.append(functions.threshold(1))
		#    f.append(functions.indicator(4))
		    f.append(functions.nor)
		return f

    def f0(self, g, s, indexList, i):
		image = s[0].x
		return state.State(image)
    def f1(self, g, s, indexList, i):
		image = s[0].x and s[3].x or s[6].x
		return state.State(image)
    def f2(self, g, s, indexList, i):
		image = s[0].x
		return state.State(image)
    def f3(self, g, s, indexList, i):
		image = s[4].x and s[2].x and (not s[5].x)
		return state.State(image)
    def f4(self, g, s, indexList, i):
		image = s[2].x and s[1].x
		return state.State(image)
    def f5(self, g, s, indexList, i):
		image = s[4].x
		return state.State(image)
    def f6(self, g, s, indexList, i):
		image = s[4].x
		return state.State(image)


    def GetGraph(self) :
    	return self.g
                
    def GetFunctionList(self) :
    	return self.f
                    
    def GetBibtex(self) :
    	return self.bibtex
                
    def GetName(self) :
    	return self.name
                    
    def GetDomain(self) :
    	return self.domain
               
class MammalianCellCyclePBN:
    def __init__(self) :
    	self.bibtex = """@article{qian2009long,
  	title={On the long-run sensitivity of probabilistic Boolean networks},
  	author={Qian, Xiaoning and Dougherty, Edward R},
  	journal={Journal of theoretical biology},
  	volume={257},
  	number={4},
  	pages={560--577},
  	year={2009},
  	publisher={Elsevier}
	}
        """
	self.name = "MammalianCellCyclePBN"
    	self.description = "wild-type mammalian cell cycle network"
    	self.domain = "biology"
    	self.g = self.CreateGraph()
    	self.f = self.SetFunctionList()

    def CreateGraph(self) :
    	Y = nx.DiGraph()
    	edgeSet = [("CycD" , "CycD"), ("CycD" , "Rb"), ("CycD" , "p27"), 
		   ("Rb", "CycE"), ("Rb", "E2F"), ("Rb", "CycA"), 
		   ("p27", "p27"), ("p27", "Rb"), ("p27" , "Cdh1"), ("p27" , "E2F"), ("p27" , "CycE"),
		   ("E2F", "CycA"), ("E2F", "CycE"), 
	           ("CycE", "CycE"), ("CycE", "Rb"), ("CycE", "p27"),
		   ("CycA", "CycA"), ("CycA", "Rb"), ("CycA", "E2F"), ("CycA", "p27"), ("CycA", "Cdh1"), ("CycA", "UbcH10"), 
		   ("Cdc20", "CycB"), ("Cdc20", "UbcH10"), ("Cdc20", "CycA"), ("Cdc20", "Cdh1"),
		   ("Cdh1", "CycA"), ("Cdh1", "CycB"), ("Cdh1", "Cdc20"), ("Cdh1", "CycA"), ("Cdh1", "UbcH10"), 
		   ("UbcH10", "UbcH10"), ("UbcH10", "CycA"), 
		   ("CycB", "UbcH10"), ("CycB", "Cdc20"), ("CycB", "p27"), ("CycB", "Rb"), ("CycB", "E2F"),            
              ]
	
    	Y.add_edges_from(edgeSet)
            
    	self.labelMap = {"CycD" : 0 , "Rb" : 1 , "p27" : 2 , "E2F" : 3 , "CycE" : 4 , "CycA" : 5 , "Cdc20" : 6, "Cdh1" : 7, "UbcH10" : 8, "CycB" : 9}
            
    	return nx.DiGraph(nx.relabel_nodes(Y,self.labelMap))
            
    def SetFunctionList(self) :
		f = list()
		#f = [self.f0, self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9]
		for node in self.g.nodes():
	    	#    f.append(functions.threshold(1))
		#    f.append(functions.indicator(4))
		    f.append(functions.nor)
		return f

    def f0(self, g, s, indexList, i):
		image = s[0].x
		return state.State(image)
    def f1(self, g, s, indexList, i):
		image = ((not s[0].x) and (not s[4].x) and (not s[5].x)) or (s[2].x and (not s[0].x) and (not s[9].x)) 
		return state.State(image)
    def f2(self, g, s, indexList, i):
		image = ((not s[0].x) and (not s[4].x) and (not s[5].x)) or (s[2].x and not(s[4].x and s[5].x) and (not s[0].x) and (not s[9].x))
		return state.State(image)
    def f3(self, g, s, indexList, i):
		image = ((not s[1].x) and (not s[5].x) and (not s[9].x)) or (s[2].x and (not s[1].x) and (not s[9].x))
		return state.State(image)
    def f4(self, g, s, indexList, i):
		image = s[3].x and (not s[1].x)
		return state.State(image)
    def f5(self, g, s, indexList, i):
		image = (s[3].x and (not s[1].x) and (not s[6].x) and not(s[7].x and s[8].x)) or (s[5].x and (not s[1].x) and (not s[6].x) and not(s[7].x and s[8].x))
		return state.State(image)
    def f6(self, g, s, indexList, i):
		image = s[9].x
		return state.State(image)
    def f7(self, g, s, indexList, i):
		image = ((not s[5].x) and (not s[9].x)) or s[6].x or (s[2].x and (not s[9].x))
 		return state.State(image)
    def f8(self, g, s, indexList, i):
		image = (not s[7].x) or (s[7].x and s[8].x and (s[6].x or s[5].x or s[9].x))
		return state.State(image)
    def f9(self, g, s, indexList, i):
		image = (not s[6].x) and (not s[7].x)
		return state.State(image)


    def GetGraph(self) :
    	return self.g
                
    def GetFunctionList(self) :
    	return self.f
                    
    def GetBibtex(self) :
    	return self.bibtex
                
    def GetName(self) :
    	return self.name
                    
    def GetDomain(self) :
    	return self.domain

class generalizedThreshold :

    def __init__(self, k ) :
        self.k = k

    def __call__(self, g, s, indexList, i) :
        sum = 0
        for j in indexList :
	        sum += s[j].x*g[j][i]['weight']
        return state.State( 0 if sum < self.k else 1, 2)

def main() :
    M = MendozaAlvarezBuylla()
    X = M.GetGraph()
    activity = list()

    for node in X.nodes() :
        f = M.GetFunctionList()
        A = Activity.Activity(X, f, node)
        A.ComputeActivity()
        activity.append(A.GetActivity())
    print "Average activity for network %s:" %M.GetName()
    print activity

    M = I5GroupTTSS()
    X = M.GetGraph()
    activity = list()

    for node in X.nodes() :
        f = M.GetFunctionList()
        A = Activity.Activity(X, f, node)
        A.ComputeActivity()
        activity.append(A.GetActivity())
    print "Average activity for network %s:" %M.GetName()
    print activity

    M = MammalianCellCyclePBN()
    X = M.GetGraph()
    activity = list()

    for node in X.nodes() :
        f = M.GetFunctionList()
        A = Activity.Activity(X, f, node)
        A.ComputeActivity()
        activity.append(A.GetActivity())
    print "Average activity for network %s:" %M.GetName()
    print activity

if __name__ == "__main__" :
    main()

