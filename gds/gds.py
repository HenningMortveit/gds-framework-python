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
        self.blockSequence = None

    def NumStates(self) :
        limit = self.tupleConverter.limit
        ng = util.enumeration.NTupleGenerator(limit)
        return ng.Num()


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
        self.blockSequence = None

    def SetBlockSequence(self, blockSequence) :
        s = set()
        for b in blockSequence :
            for i in b :
                s.add(i)
        n = set( self.g.nodes() )
        if not s.issubset(n) :
            print "Replace by an exception"
        self.blockSequence = blockSequence
        self.sequence = None;

    def SetParallel(self) :
        self.sequence = None
        self.blockSequence = None

    def Evaluate(self, x) :
        """Evaluate the GDS map at x and return the image."""
        if self.sequence != None :
            y = copy.deepcopy(x)
            return self.EvaluateSequential(y)
        elif self.blockSequence != None :
            y = copy.deepcopy(x)
            return self.EvaluateBlockSequential(y)
        else :
            return self.EvaluateParallel(x)

    def EvaluateBlockSequential(self, x) :
        for block in self.blockSequence :
            if( len(block) > 1 ) :
                y = copy.deepcopy(x)
                for i in block :
                    x[i] = self.f[i](self.g, y, self.iMap[i], i)
            else :
                i = block[0]
                x[i] = self.f[i](self.g, x, self.iMap[i], i)
        return x

    def EvaluateParallel(self, x) :
        y = []
        for i in range(0, self.dim) :
            y.append( self.f[i](self.g, x, self.iMap[i], i) )
        return y

    def EvaluateSequential(self, x) :
        for i in self.sequence :
            x[i] = self.f[i](self.g, x, self.iMap[i], i)
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

