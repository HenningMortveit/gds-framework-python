import gds.util.enumeration
import gds.util.file_io
import gds.state
import gds.graphs
import gds.functions
import gds.gds
import gds.algorithms
import gds.state_algorithms
import gds.phase_space
import gds.sequence
import sys
sys.path.append("/home/sichao/svn/Sichao/code")
from XMLConfig import *
from DOE import *
from statDesign import *
from gds.gdsConfig import *

def genDOE(baseConfigFile, designType, designRegion, doeName, outFolder) :
    cs = loadConfig(baseConfigFile)
    doe = configToDOE(cs)
    for key in designRegion:
        levels = designRegion[key]
        doe.setLevels(key, levels)
    saveDOE(doe, doeName)
    if designType == "fullFact" :
        namePattern = outFolder + "gdsConfig-cell%s.xml" %("%i")
        samples = fullFact(doe)
        genConfig(cs, doe, samples, namePattern)

def main() :
    baseConfigFile = "/home/sichao/svn/Sichao/Thesis/DigitalObjects/gdsConfig.xml"
    designType = "fullFact" 
    designRegion = dict()
    designRegion["graph"] = ["/home/sichao/gds/gds/graphs/g1","/home/sichao/gds/gds/graphs/g2"]
    designRegion["functionSpec/f1/thresholdValue"] = [1,2,3]
    outFolder = "./ExpDesign/"
    doeName = outFolder + "gdsFullFact.xml" 
    genDOE(baseConfigFile, designType, designRegion, doeName, outFolder)
    cs = loadConfig("ExpDesign/gdsConfig-cell0.xml")
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
    
