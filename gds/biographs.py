################################################################################
# Feb. 4 2014
# This module stores a set of biology networks. A network object has a graph, 
# a list of functions, and information such as bibtex reference,
# name, domain("biology" for this module), etc.
################################################################################

import networkx as nx
import matplotlib.pyplot as plt
import gds
import state
import functions
import sys

import Activity

class LacOperon() :
    """Description:

    HSM: 14 October 2015. Note that if there are modifications or
    corrections, then iMap and function definitions must be kept
    consistent. There is no link between them. The same applies to the
    network.
    
    """ 
   
    def __init__(self, Ge, Le, Lem) :

        self.bibtex = """@inproceedings{Montalva:14,
  			title={Attraction basins in a lac operon model under different update schedules},
  			author={Montalva, Marco and Ruz, Gonzalo A. and Goles, Eric},
  			booktitle={ALIFE 14: Proceedings of the Fourteenth Interantional Conference on the Synthetsis and Simulation of Living Systems},

  			year={2014},
                        doi = {http://dx.doi.org/10.7551/978-0-262-32621-6-ch109}
			}
			"""
	self.name = "LacOperon"
        self.description = "Veliz-Cuba and Stigler's lac operon model as reported by Montalva et al"
        self.domain = "biology"

        self.SetParams(Ge, Le, Lem)
        self.iMap = []   # index map as for GDS
        self.g = self.CreateGraph()
        self.f = self.SetFunctionList()
        self.F = self.ConstructGDS()

    def SetParams(self, Ge, Le, Lem) :
        self.Ge = Ge
        self.Le = Le
        self.Lem = Lem

    def CreateGraph(self) :

        self.iMap = dict()   # index map as for GDS

    	X = nx.DiGraph()

    	edges = [("C", "M",  {"weight":1}), 
                 ("M","B",   {"weight":1}),
                 ("M","P",   {"weight":1}),
                 ("B","A",   {"weight":1}),
                 ("P","L",   {"weight":1}),
                 ("P","Lm",  {"weight":1}),
                 ("R","Rm",  {"weight":1}),
                 ("R","M",   {"weight":1}),
                 ("A","R",   {"weight":1}),
                 ("A","Rm",  {"weight":1}),
                 ("L","A",   {"weight":1}),
                 ("L","Am",  {"weight":1}),
	     	 ("Am","R",  {"weight":1}),
                 ("Am","Rm", {"weight":1}),
	     	 ("Rm","M",  {"weight":1}), 
                 ("Lm","Am", {"weight":1})
            	]
        
    	X.add_edges_from(edges)

    	self.labelMap = {
            "M"  : 0, 
            "P"  : 1, 
            "B"  : 2, 
            "C"  : 3,
            "R"  : 4, 
            "Rm" : 5, 
            "A"  : 6, 
            "Am" : 7,
            "L"  : 8, 
            "Lm" : 9
        }

        n = len(self.labelMap)

        #for i in range(0, n) :
        #    self.iMap.append([])

        i = self.labelMap

        self.iMap[ i["M"] ]  = [ i["C"], i["R"], i["Rm"] ]
        self.iMap[ i["P"] ]  = [ i["M"] ]
        self.iMap[ i["B"] ]  = [ i["M"] ]
        self.iMap[ i["C"] ]  = [  ]
        self.iMap[ i["R"] ]  = [ i["A"], i["Am"] ]
        self.iMap[ i["Rm"] ] = [ i["A"], i["Am"], i["R"] ]
        self.iMap[ i["A"] ]  = [ i["L"], i["B"] ]
        self.iMap[ i["Am"] ] = [ i["L"], i["Lm"] ]
        self.iMap[ i["L"] ]  = [ i["P"] ]
        self.iMap[ i["Lm"] ] = [ i["P"] ]

        print self.iMap

#        print "iMap", len(self.labelMap), self.iMap

    	return nx.DiGraph(nx.relabel_nodes(X,self.labelMap))  

 
    def fM(self, g, s, indexList, i) :
        i = indexList # self.iMap[ self.labelMap["M"] ]
        image =  s[ i[0] ].x and (not s[ i[1] ].x) and (not s[ i[2] ].x)
        #i = self.labelMap
        #image =  s[ i["C"] ].x and (not s[ i["R"] ].x) and (not s[ i["Rm"] ].x)
        return state.State(int(image), 2)

    def fP(self, g, s, indexList, i) :
        i = indexList #  self.iMap[self.labelMap["P"] ]
        image = s[ i[0] ].x 
        #i = self.labelMap
        #image = s[ i["M"] ].x 
        return state.State(int(image))

    def fB(self, g, s, indexList, i) :
        i =  indexList # self.iMap[ self.labelMap["B"] ]
        image = s[ i[0] ].x 
        #i = self.labelMap
        #image = s[ i["M"] ].x 
        return state.State(int(image))

    def fC(self, g, s, indexList, i) :
        image = not self.Ge
        return state.State(int(image))

    def fR(self, g, s, indexList, i) :
        i = indexList #  self.iMap[ self.labelMap["R"] ]
        image = (not s[ i[0] ].x) and (not s[ i[1] ].x)
        #i = self.labelMap
        #image = (not s[ i["A"] ].x) and (not s[ i["Am"] ].x)
        return state.State(int(image))

    def fRm(self, g, s, indexList, i) :
        i = indexList #  self.iMap[ self.labelMap["Rm"] ]
        image = ((not s[ i[0] ].x) and (not s[ i[1] ].x)) or (s[ i[2] ].x)
        #i = self.labelMap
        #image = ((not s[ i["A"] ].x) and (not s[ i["Am"] ].x)) or (not s[ i["R"] ].x)
        return state.State(int(image))

    def fA(self, g, s, indexList, i):
        i = indexList #  self.iMap[ self.labelMap["A"] ]
        image = s[ i[0] ].x and s[ i[1] ].x
        #i = self.labelMap
        #image = s[ i["L"] ].x and s[ i["B"] ].x
        return state.State(int(image))

    def fAm(self, g, s, indexList, i):
        i = indexList #  self.iMap[ self.labelMap["Am"] ]
        image = s[ i[0] ].x or s[ i[1] ].x
        #i = self.labelMap
        #image = s[ i["L"] ].x or s[ i["Lm"] ].x
        return state.State(int(image))

    def fL(self, g, s, indexList, i):
        i = indexList #  self.iMap[ self.labelMap["L"] ]
        image = s[ i[0] ].x and self.Le and (not self.Ge)
        #i = self.labelMap
        #image = s[ i["P"] ].x and self.Le and (not self.Ge)
        return state.State(int(image))

    def fLm(self, g, s, indexList, i):
        i = indexList #  self.iMap[ self.labelMap["Lm"] ]
        image = ( (self.Lem and s[ i[0] ].x) or self.Le ) and (not self.Ge)
        #i = self.labelMap
        #image = ( (self.Lem and s[ i["P"] ].x) or self.Le ) and (not self.Ge)
        return state.State(int(image))


    def SetFunctionList(self) :
	f = [self.fM, self.fP, self.fB, self.fC, self.fR, 
             self.fRm, self.fA, self.fAm, self.fL, self.fLm]
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

    def GetIMap(self) :
        return self.iMap

    def ConstructGDS(self) :

        n = nx.number_of_nodes(self.g)
        stateObject = n * [gds.state.State(0, 2)]

        gds1 = gds.GDS(g = self.g, f = self.f, 
                       stateObjectList = stateObject, 
                       iMap = self.iMap)
        return gds1


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
    lacOperon = LacOperon(0, 0, 0)
    X = lacOperon.GetGraph()
    f = lacOperon.GetFunctionList()
    iMap = lacOperon.GetIMap()
    
    print "activity 0:", Activity.Activity(X, f, 0, iMap).GetActivity()
    
    sys.exit(0)
    

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

