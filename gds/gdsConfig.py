import sys
sys.path.append("/home/sichao/svn/Sichao/code")

from util.file_io import *
import XMLConfig
import gds
import algorithms
import functions
import phase_space
import networkx

class gdsConfig :
    def __init__(self, cs) :
        self.cs = cs
        self.configName = cs.configName
        self.methodName = cs.methodName
        self.description = cs.description
        self.baseConfigFile = cs.baseConfigFile
        self.graph = self.setGraph()
        self.functionList = []
        self.functionList = self.setFunctionList()
        self.doCircle = XMLConfig.str2bool(cs.parameterDict["doCircle"].value)
        self.setSchedule()
        self.gds = self.setGDS()

    def setGraph(self) :
        fileName = self.cs.parameterDict["graph"].value
        return LoadObject(fileName)

    def setFunction(self, func) :
        if func.value =="threshold" :
            try:
                t = int(func.subParamList[0].value)
            except KeyError:
                print "Failed to load threshold value!"
            f = functions.threshold(t)
        elif func.value =="indicator" :
            try:
                t = int(func.subParamList[0].value)
            except KeyError:
                print "Failed to load threshold value!"
            f = functions.indicator(t)
        elif func.value =="biThreshold" :
            try:
                kup = int(func.subParamList[0].value)
                kdown = int(func.subParamList[1].value)
            except KeyError:
                print "Failed to load threshold value!"
            f = functions.biThreshold(kup, kdown)
        elif func.value =="inverseThreshold" :
            try:
                t = int(func.subParamList[0].value)
            except KeyError:
                print "Failed to load threshold value!"
            f = functions.inverseThreshold(t)
        elif func.value =="dynBiThreshold" :
            try:
                D01up = int(func.subParamList[0].value)
                D10up = int(func.subParamList[1].value)
                D01down = int(func.subParamList[2].value)
                D10down = int(func.subParamList[3].value)
            except KeyError:
                print "Failed to load threshold value!"
            f = functions.dynBiThreshold(D01up, D10up, D01down, D10down)
        elif func.value =="wolfram" :
            try:
                r = int(func.subParamList[0].value)
            except KeyError:
                print "Failed to load rule number!"
            f = functions.wolfram(r)
        elif func.value == "parity" :
            f = functions.parity
        elif func.value == "majority" :
            f = functions.majority
        elif func.value == "nor" :
            f = functions.nor
        elif func.value == "nand" :
            f = functions.nand
	else : 
            raise Exception("""Error: Unknown function type! Available options: 
                   <threshold, indicator, biThreshold, inverseThreshold, dynBiThreshold, wolfram, parity, majority, nor, nand>""")
        return f

    def setFunctionList(self) :
        n = len(self.graph.nodes())
        funcType = self.cs.parameterDict["functionSpec"].value
        functions = self.cs.parameterDict["functionSpec"].subParamList
        functionList = []
        if funcType == "uniform" :
            func = functions[0]
            f = self.setFunction(func)
            for i in range(n) :
                functionList.append(f)
        elif funcType == "nonuniform" :
            functions = self.cs.parameterDict["functionSpec"].subParamList
            for func in functions:
                f = self.setFunction(func)
                functionList.append(f)
            if len(functionList) != n :
                raise Exception("Error: Number of functions and nodes does not match!")
        return functionList

    def setSchedule(self) :
        self.schedule = self.cs.parameterDict["schedule"].value
        if self.schedule == "sequential" :
            self.permutation = []
            seq = self.cs.parameterDict["schedule/permutation"].value.split(',')
            for i in seq :
                self.permutation.append(int(i))
        elif self.schedule == "parallel" :
            pass
        else :
            raise Exception("Error: Unknown schedule! Available options: <sequential, parallel>")

    def setGDS(self) :
        n = len(self.graph.nodes())
        stateObj = n * [gds.state.State(0, 2)]
        GDS = gds.GDS(self.graph, self.functionList, stateObj, self.doCircle)
        if self.schedule == "sequential" :
            GDS.SetSequence(self.permutation)
        elif self.schedule == "parallel" :
            GDS.SetParallel()
        return GDS    
 

def main() :
    #X = gds.graphs.CircleGraph(4)
    #X.add_edge(0, 2)
    #DumpObject("/home/sichao/gds/gds/graphs/cir4", X)
    #sys.exit(0)
    cs = XMLConfig.loadConfig("/home/sichao/svn/Sichao/Thesis/DigitalObjects/gdsConfig.xml")
    config = gdsConfig(cs)
    gds1 = config.gds

    transitions = algorithms.GenerateTransitions(gds1)
    fixedPoints = algorithms.FixedPoints(gds1, transitions)

    p = phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: "
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

    print "Periodic points: "
    for i, cycle in enumerate(periodicPoints) :
        print i
        for j in cycle :
            print gds1.IntegerToState(j)

    print "Components: ", components

    for x,y in enumerate(transitions) :
        print gds1.IntegerToState(x), "->", gds1.IntegerToState(y)

if __name__ == "__main__" :
    main()
