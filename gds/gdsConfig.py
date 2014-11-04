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
        self.function = self.setFunction()
        self.doCircle = str2bool(cs.parameterDict["doCircle"].value)
        self.setSchedule()

    def setGraph(self) :
        fileName = self.cs.parameterDict["graph"].value
        return LoadObject(fileName)

    def setFunction(self) :
        func = self.cs.parameterDict["function"].value
        if func=="threshold" :
            try:
                t = int(self.cs.parameterDict["threshold"].value)
            except KeyError:
                print "Failed to load parameter<%s>" %func
            function = functions.threshold(t)
            return function
    
    def setSchedule(self) :
        self.schedule = self.cs.parameterDict["schedule"].value
        if self.schedule == "sequential" :
            self.permutation = list()
            seq = self.cs.parameterDict["permutation"].value.split(',')
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
    functions = n * [config.function]
    print config.doCircle
    gds1 = gds.GDS(config.graph, functions, stateObj, config.doCircle)

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
