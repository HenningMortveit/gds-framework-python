#
# GDS function classes.
#
# Convention: The argument consists of:
#   x: the system state
#   i: the vertex to be evaluated
#   indexList: n[i]

import state

# ------------------------------------------------------------

def parity(s, indexList, i) :
    """Boolean parity function (sum modulo 2)"""

    sum = 0
    for k in indexList :
        sum += s[k].x
    return state.State(sum % 2, 2)

def majority(s, indexList, i) :
    """Boolean parity function (sum modulo 2)"""

    sum = 0
    for k in indexList :
        sum += s[k].x

    if sum >= 0.5*len(indexList) :
        return state.State(1, 2)
    else :
        return state.State(0, 2)


def nor(s, indexList, i) :
    """Boolean nor function"""

    sum = 0
    for k in indexList :
        sum += s[k].x
    return state.State(1 if sum == 0 else 0, 2)

def nand(s, indexList, i) :
    """Boolean nand function"""

    sum = 0
    l = len(indexList)
    for k in indexList :
        sum += s[k].x
    return state.State(0 if sum == l else 1, 2)


class threshold :
    """Binary threshold rule."""

    def __init__(self, k ) :
        self.k = k

    def __call__(self, s, indexList, i) :
        sum = 0
        for j in indexList :
            sum += s[j].x
        return state.State( 0 if sum < self.k else 1, 2)

class biThreshold :
    """Binary bi-threshold rule."""

    def __init__(self, kup, kdown ) :
        self.kup = kup
        self.kdown = kdown

    def __call__(self, s, indexList, i) :
        sum = 0
        for j in indexList :
            sum += s[j].x

        if s[i].x == 0 and sum >= self.kup :
            return state.State(1, 2)
        elif s[i].x == 1 and sum < self.kdown :
            return state.State(0, 2)
        else :
            return s[i]


class inverseThreshold :
    """Inverse binary threshold rule."""

    def __init__(self, k ) :
        self.k = k

    def __call__(self, s, indexList, i) :
        sum = 0
        for j in indexList :
            sum += s[j].x
        return state.State( 1 if sum <= self.k else 0, 2)

class dynBiThreshold :
    """SW: Dynamic bi-threshold rule"""

    def __init__(self, D01up, D10up, D01down, D10down) :
        self.D01up = D01up
        self.D10up = D10up
        self.D01down = D01down
        self.D10down = D10down

    def __call__(self, s, indexList, i) :
        sum = 0
        for j in indexList :
            sum += s[j].x

        if s[i].x == 0 and sum >= s[i].kup :
            s[i].kup = s[i].kup + self.D01up
            s[i].kdown = s[i].kdown + self.D01down
            return state.StateDynBiT(1, s[i].kup, s[i].kdown, s[i].degree)
        elif s[i].x == 1 and sum < s[i].kdown :
            s[i].kup = s[i].kup + self.D10up
            s[i].kdown = s[i].kdown + self.D10down
            return state.StateDynBiT(0, s[i].kup, s[i].kdown, s[i].degree)
        else :
            return s[i]



# Wolfram's/vonNeumann's basic cellular automata rules.

#
# x(i-1) x(i) x(i+1)  111 110 101 100 011 010 001 000
#        f            a7  a6  a5  a4  a3  a2  a1  a0
# encoding is: sum(i) a_i 2^i
#

class wolfram :
    """Elementary CA rule aka wolfram rule."""

    def __init__(self, ruleNumber ) :
        # Test for 0 <= ruleNumber <= 255 ...
        self.ruleNumber = ruleNumber
        self.ruleTable = []
        for i in range(0, 8) :
            self.ruleTable.append( 1 if self.ruleNumber & (1<<i) > 0 else 0 )

    def __call__(self, s, indexList, i) :
        idx = s[indexList[0]].x * 4 \
            + s[indexList[1]].x * 2 \
            + s[indexList[2]].x * 1
        return state.State(self.ruleTable[idx], 2)


# Dynamic threshold functions:

def f_up(s, indexList, i) :
    """Increasing threshold function."""

    sum = 0
    for k in indexList :
        sum += s[k].x

    x = 0 if sum < s[i].k else 1

    k = s[i].k + 1 if (s[i].x == 0           and
                       x == 1                and
                       s[i].k <= s[i].degree      ) else s[i].k

    return state.StateDynT(x, k, s[i].degree)


def f_down(s, indexList, i) :
    """Decreasing threshold function."""

    sum = 0
    for k in indexList :
        sum += s[k].x

    x = 0 if sum < s[i].k else 1

    k = s[i].k - 1 if (s[i].x == 1 and
                       x == 0      and
                       s[i].k > 1        ) else s[i].k

    return state.StateDynT(x, k, s[i].degree)


def f_up_down(s, indexList, i) :
    """Mixed threshold function."""

    sum = 0
    for k in indexList :
        sum += s[k].x

    x = 0 if sum < s[i].k else 1

    k = s[i].k

    if s[i].x == 1 and x == 0 and s[i].k > 1 :
        k = s[i].k - 1
    elif s[i].x == 0 and x == 1 and s[i].k <= s[i].degree  :
        k = s[i].k + 1

    return state.StateDynT(x, k, s[i].degree)

