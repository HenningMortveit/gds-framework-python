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
import glob
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
        namePattern = outFolder + "config_bithreshold_cell%s.xml" %("%i")
        samples = fullFact(doe)
        genConfig(cs, doe, samples, namePattern)

def main() :
    baseConfigFile = "./BiThresholdExpDesign/biThresholdBaseConfig.xml"
    designType = "fullFact" 
    designRegion = dict()
    designRegion["functionSpec/function/kup"] = [1,2,3]
    designRegion["functionSpec/function/kdown"] = [1,2,3]
    doeName = "./BiThresholdExpDesign/doe_bithreshold_fullfact.xml"
    configFolder = "./BiThresholdExpDesign/config/"
    genDOE(baseConfigFile, designType, designRegion, doeName, configFolder)

    outputFile = "./BiThresholdExpDesign/output"
    output = open(outputFile, 'w')
    configFileList = glob.glob(configFolder+"config_bithreshold_cell[0-9]*.xml")
    for configFile in configFileList :
        cs = loadConfig(configFile)
        config = gdsConfig(cs)
        gds1 = config.gds
        transitions = algorithms.GenerateTransitions(gds1)
        fixedPoints = algorithms.FixedPoints(gds1, transitions)
        output.write("###############################################\n")
        output.write("kup:" + cs.parameterDict["functionSpec/function/kup"].value + "\n")
        output.write("kdown:" + cs.parameterDict["functionSpec/function/kdown"].value + "\n")
        output.write("Number of fixed points:" + str(len(fixedPoints)) + "\n")
    output.close()


    #p = phase_space.PhaseSpace(gds1)

    #fixedPoints = p.GetFixedPoints()
    #periodicPoints = p.GetPeriodicPoints()
    #components = p.GetComponents()

    #print "Fixed points: "
    #for i in fixedPoints :
    #    print i, gds1.IntegerToState(i)

    #print "Periodic points: "
    #for i, cycle in enumerate(periodicPoints) :
    #    print i
    #    for j in cycle :
    #        print gds1.IntegerToState(j)

    #print "Components: ", components

    #for x,y in enumerate(transitions) :
    #    print gds1.IntegerToState(x), "->", gds1.IntegerToState(y)


if __name__ == "__main__" :
    main()
    
