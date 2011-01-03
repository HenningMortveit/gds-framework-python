#
# Core GDS class.
#

import copy

import util.enumeration
import state
import state_algorithms
import graphs
import graph_algorithms
import functions

class GDS :
    def __init__(self, g, f, stateObjectList, circleFlag = False) :
        self.stateObjectList = None
        self.tupleConverter = None
        self.SetGraph(g, stateObjectList, circleFlag)
        self.SetMap(f)
        self.sequence = None


    def SetGraph(self, g, stateObjectList, circleFlag = False) :
        self.g = g
        self.iMap = graph_algorithms.CreateIndexMap(g)
        self.dim = len( self.g.nodes() )
        if circleFlag == True : # rearrange some ...
            self.iMap[0] = [self.dim-1, 0, 1]
            self.iMap[self.dim-1] = [self.dim-2, self.dim-1, 0]
        self.SetStateObjectList(stateObjectList)

    def SetStateObjectList(self, stateObjectList) :
        self.stateObjectList = stateObjectList

        limit = []
        for i in stateObjectList :
            limit.append( i.Num() )

        self.tupleConverter = util.enumeration.TupleConverter(limit)


    def SetMap(self, f ) :
        if not len(f) == self.dim :
            print "Replace this by an exception"
        self.f = f

    def SetSequence(self, sequence) :
        s = set(sequence)
        n = set( self.g.nodes() )
        if not s.issubset(n) :
            print "Replace by an exception"
        self.sequence = sequence

    def SetParallel(self) :
        self.sequence = None

    def Evaluate(self, x) :
        """Evaluate the GDS map at x and return the image."""
        if self.sequence == None :
            return self.EvaluateParallel(x)
        else :
            y = copy.deepcopy(x)
            return self.EvaluateSequential(y)

    def EvaluateParallel(self, x) :
        y = []
        for i in range(0, self.dim) :
            y.append( self.f[i](x, self.iMap[i], i) )
        return y

    def EvaluateSequential(self, x) :
        for i in self.sequence :
            x[i] = self.f[i](x, self.iMap[i], i)
        return x

    def GetDim(self) :
        return self.dim;

    def IntegerToState(self, i) :
        indexState = self.tupleConverter.IndexToTuple(i)
        x = state_algorithms.IndexStateTupleToRegularStateTuple(indexState, self.stateObjectList)
        return x

    def StateToInteger(self, x) :
        indexState = state_algorithms.RegularStateTupleToIndexStateTuple(x,  self.stateObjectList)
        i = self.tupleConverter.TupleToIndex(indexState)
        return i

# -- End --
