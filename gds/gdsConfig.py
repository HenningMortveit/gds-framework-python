import sys
sys.path.append("/home/sichao/gitlab/sichao/code/src/python_package")

from util.file_io import *
import xml_config
import gds
import algorithms
import functions
import phase_space
import networkx

class gdsConfig :
    def __init__(self, cs) :
        self.cs = cs
        self.config_name = cs.config_name
        self.method_name = cs.method_name
        self.description = cs.description
        self.base_config_file = cs.base_config_file
        self.graph = self.set_graph()
        self.function_list = []
        self.function_list = self.set_function_list()
        self.do_circle = xml_config.str2bool(cs.parameter_dict["doCircle"].value)
        self.set_schedule()
        self.gds = self.set_gds()

    def set_graph(self) :
        file_name = self.cs.parameter_dict["graph"].value
        return LoadObject(file_name)

    def set_function(self, func) :
        if func.value =="threshold" :
            try:
                t = int(func.sub_param_list[0].value)
            except KeyError:
                print "Failed to load threshold value!"
            f = functions.threshold(t)
        elif func.value =="indicator" :
            try:
                t = int(func.sub_param_list[0].value)
            except KeyError:
                print "Failed to load threshold value!"
            f = functions.indicator(t)
        elif func.value =="biThreshold" :
            try:
                kup = int(func.sub_param_list[0].value)
                kdown = int(func.sub_param_list[1].value)
            except KeyError:
                print "Failed to load threshold value!"
            f = functions.biThreshold(kup, kdown)
        elif func.value =="inverseThreshold" :
            try:
                t = int(func.sub_param_list[0].value)
            except KeyError:
                print "Failed to load threshold value!"
            f = functions.inverseThreshold(t)
        elif func.value =="dynBiThreshold" :
            try:
                D01up = int(func.sub_param_list[0].value)
                D10up = int(func.sub_param_list[1].value)
                D01down = int(func.sub_param_list[2].value)
                D10down = int(func.sub_param_list[3].value)
            except KeyError:
                print "Failed to load threshold value!"
            f = functions.dynBiThreshold(D01up, D10up, D01down, D10down)
        elif func.value =="wolfram" :
            try:
                r = int(func.sub_param_list[0].value)
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

    def set_function_list(self) :
        n = len(self.graph.nodes())
        func_type = self.cs.parameter_dict["functionSpec"].value
        functions = self.cs.parameter_dict["functionSpec"].sub_param_list
        function_list = []
        if func_type == "uniform" :
            func = functions[0]
            f = self.set_function(func)
            for i in range(n) :
                function_list.append(f)
        elif func_type == "nonuniform" :
            functions = self.cs.parameter_dict["functionSpec"].sub_param_list
            for func in functions:
                f = self.set_function(func)
                function_list.append(f)
            if len(function_list) != n :
                raise Exception("Error: Number of functions and nodes does not match!")
        return function_list

    def set_schedule(self) :
        self.schedule = self.cs.parameter_dict["schedule"].value
        if self.schedule == "sequential" :
            self.permutation = []
            seq = self.cs.parameter_dict["schedule/permutation"].value.split(',')
            for i in seq :
                self.permutation.append(int(i))
        elif self.schedule == "parallel" :
            pass
        else :
            raise Exception("Error: Unknown schedule! Available options: <sequential, parallel>")

    def set_gds(self) :
        n = len(self.graph.nodes())
        stateObj = n * [gds.state.State(0, 2)]
        GDS = gds.GDS(self.graph, self.function_list, stateObj, self.do_circle)
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
    cs = xml_config.load_config("/home/sichao/svn/Sichao/Thesis/DigitalObjects/gdsConfig.xml")
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
