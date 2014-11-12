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
    designRegion["graph"] = ["home/sichao/gds/gds/graphs/g1","home/sichao/gds/gds/graphs/g2"]
    designRegion["functionSpec/f1/thresholdValue"] = [1,2,3]
    outFolder = "./ExpDesign/"
    doeName = outFolder + "gdsFullFact.xml" 
    genDOE(baseConfigFile, designType, designRegion, doeName, outFolder)


if __name__ == "__main__" :
    main()
    
