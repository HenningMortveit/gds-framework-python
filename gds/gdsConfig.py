import sys
sys.path.append("/home/sichao/svn/Sichao/code")

from XMLConfig import *
from util.file_io import *
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
        self.setFunctionList()
        self.doCircle = str2bool(cs.parameterDict["doCircle"].value)
        self.setSchedule()

    def setGraph(self) :
        fileName = self.cs.parameterDict["graph"].value
        return LoadObject(fileName)

    def setFunction(self, func) :
        if func.value =="threshold" :
            try:
                t = int(func.subParamList[0].value)
            except KeyError:
                print "Failed to load parameter<%s>" %func
            function = functions.threshold(t)
            return function

    def setFunctionList(self) :
        n = len(self.graph.nodes())
        funcType = self.cs.parameterDict["functionSpec"].value
        functions = self.cs.parameterDict["functionSpec"].subParamList
        if funcType == "uniform" :
            func = functions[0]
            f = self.setFunction(func)
            for i in range(n) :
                self.functionList.append(f)
        elif funcType == "nonuniform" :
            functions = self.cs.parameterDict["functionSpec"].subParamList
            for func in functions:
                f = self.setFunction(func)
                self.functionList.append(f)

    def setSchedule(self) :
        self.schedule = self.cs.parameterDict["schedule"].value
        if self.schedule == "sequential" :
            self.permutation = []
            seq = self.cs.parameterDict["schedule/permutation"].value.split(',')
            for i in seq :
                self.permutation.append(i)
        print self.permutation
 

def main() :
    pi = [0,1,2,3];
    X = gds.graphs.CircleGraph(4)

    DumpObject("/home/sichao/gds/gds/graphs/g1", X)
    cs = loadConfig("/home/sichao/svn/Sichao/Thesis/DigitalObjects/gdsConfig.xml")
    config = gdsConfig(cs)
    n = len(config.graph.nodes())
    stateObj = n * [gds.state.State(0, 2)]
    print config.doCircle
    gds1 = gds.GDS(config.graph, config.functionList, stateObj, config.doCircle)

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
main()
