import os
import math
import gds
import algorithms
import graphs

def ComputeActivity (iNode, gds):
    """Compute alpha_{F,i}"""
    transitions = algorithms.GenerateTransitions(gds)
    diff = 0
    for x,y in enumerate(transitions) :
        state = gds.IntegerToState(x)
        iFlipState = state
        if (iFlipState[iNode].x == 0) :
            iFlipState[iNode].x = 1
        else :
            iFlipState[iNode].x = 0
        iFlipStateIndex = gds.StateToInteger(iFlipState)
        iFlipImageIndex = transitions[iFlipStateIndex]
        if (y != iFlipImageIndex) :
            diff = diff + 1
    activity = float(diff)/(2**gds.GetDim())
    print "different image:", diff
    return activity


def main() :
    n = 5
    X = graphs.PathGraph(n)
    doCircle = False
    #X.add_edge(1,3)

    f = n * [gds.functions.threshold(1)]
    stateObject = n * [gds.state.State(0, 2)]
    gds1 = gds.GDS(X, f, stateObject, doCircle)
    #gds1.SetSequence(pi)
    gds1.SetParallel()

    activity = ComputeActivity(2, gds1)
    print activity

if __name__ == "__main__":
    main()
