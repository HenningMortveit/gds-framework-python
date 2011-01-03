#
# About the various types of states:
#
# Num: Must return the size of the state set.
#
# StateToIndex: A bijection from the set of states to {0, 1, ...,
#   Num() - 1}.
#
# IndexToState: A bijection from {0, 1, ..., Num() - 1} to the set of
#   states.
#


"""There are two types of spaces:

  1. regular state space
  2. index state space.

Regular state space contains the "normal" tuples while index space
contains the corresponding tuples converted by using the state space
StateToIndex map.

Example: for the regular state x = (x1, ..., xn) the corresponding
index state tuple i = (i1, ..., in) are related by

  xk = stateObject[k].IndexToState(ik)

and

  ik = stateObject[k].StateToIndex(xk).


Moreover, an index tuple may be converted to a single integer and vice
versa.


"""




class State :
    """Standard state set K = {0,1,2, ..., size-1}"""

    def __init__(self, x = 0, size = 2) :
        self.x = x
        self.size = size

    def __repr__(self) :
        return "%i" % self.x

    def Num(self) :
        return self.size

    def StateToIndex(self, s) :
        return s.x

    def IndexToState(self, i) :
        return State(i, self.size)


class StateDynT :
    """State for dynamic threshold GDS. x in {0,1} and k in {1, 2,
    ..., degree + 1}"""

    def __init__(self, x = 0, k = 1, degree = 2) :
        self.x = x
        self.k = k
        self.degree = degree
        self.num = 2 * self.degree + 2

    def __repr__(self) :
        return "(%i, %i)" % (self.x, self.k)

    def Num(self) :
        return self.num

    def StateToIndex(self, s ) :
        return s.x * (s.degree+1) + (s.k - 1)

    def IndexToState(self, i) :
        x = i / (self.degree+1)
        k = (i % (self.degree + 1))+ 1
        return StateDynT(x, k, self.degree)
