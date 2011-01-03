#
# These are convenience functions from converting between different
# state representations. Except for the functions
# RegularStateTupleToIndexStateTuple and
# IndexStateTupleToRegularStateTuple, these functions are not
# optimized. If many conversions are needed, then computation time can
# be saved by creating a TupleConverter and working with the previous
# two functions.
#

import util.enumeration

def RegularStateTupleToIndexStateTuple(x, stateObjectList) :
    """See gds_state for description of tuple types."""
    i = []
    for k, s in enumerate( stateObjectList ) :
        i.append( s.StateToIndex( x[k] ) )
    return i

def IndexStateTupleToRegularStateTuple(i, stateObjectList) :
    """See gds_state for description of tuple types."""
    x = []
    for k, s in enumerate( stateObjectList ) :
        x.append( s.IndexToState( i[k] ) )
    return x

def IntegerToIndexStateTuple(i, stateObjectList, limit = None) :
    """Convert from an integer to its index state tuple
    representation."""

    l = None
    if limit != None :
        l = limit
    else :
        l = []
        for s in stateObjectList :
            l.append( s.Num() )

    tc = enumeration.TupleConverter(l)
    return tc.IndexToTuple(i)


def IndexStateTupleToInteger(i, stateObjectList, limit = None) :
    """Convert from an integer to its index state tuple
    representation."""

    l = None
    if limit != None :
        l = limit
    else :
        l = []
        for s in stateObjectList :
            l.append( s.Num() )

    tc = enumeration.TupleConverter(l)
    return tc.TupleToIndex(i)


def IntegerToRegularStateTuple(i, stateObjectList, limit = None) :
    """Convert from an integer to its regular state tuple
    representation."""

    indexTuple = IntegerToIndexStateTuple(i, stateObjectList, limit)
    x = []
    for index, s in enumerate(stateObjectList) :
        x.append( s.IndexToState( indexTuple[index] ) )

    return x

def RegularStateTupleToInteger(x, stateObjectList, limit = None) :
    """Convert from a regular state tuple to its integer
    representation."""

    indexTuple = RegularStateTupleToIndexStateTuple(x, stateObjectList)
    return IndexStateTupleToInteger(indexTuple, stateObjectList, limit)
