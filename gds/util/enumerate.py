#

class TupleConverter :
    """A class for converting n-tuples of the form (a_1, ..., a_n)
    where 0 <= a_i < m_i to integers and vice versa. The list 'limit'
    contains the m_i's."""

    def __init__(self, limit) :
        self.limit = limit    # the list of the m_i's
        self.n = len(limit)

        self.base = self.n * [0] # For conversion from tuple to index.
        k = 1
        for i in range(0, self.n) :
            self.base[i] = k
            k *= self.limit[i]

    def TupleToIndex(self, tuple) :
        i = 0
        for j in range(0, self.n) :
            i += tuple[j] * self.base[j]
        return i

    def IndexToTuple(self, v) :
        k = v
        a = self.n * [0]
        for j in range(0, self.n) :
            i = self.n - j - 1
            a[i] = k / self.base[i]
            k = k % self.base[i]
        return a



class NTupleGenerator :
    """A class for generating all n-tuples of the form (a_1, ..., a_n)
    where 0 <= a_i < m_i. Call Current() to retrieve the current
    n-tuple and then Next() to advance to the next n-tuple."""

    def __init__(self, limit) :
        self.limit = limit    # the list of the m_i's
        self.n = len(limit)
        self.current = self.n * [0] # [0, 0, 0, ... , 0]

        self.i = 0     # current n-tuple index
        self.N = 1     # total number of n-tuples.
        for num in self.limit :
            self.N *= num

        self.tupleConverter = TupleConverter(self.limit)



    def Num(self) :
        """The total number of n-tuples."""

        return self.N

    def Current(self):
        """The current n-tuple."""

        return self.current

    def Next(self) :
        """Advances the current n-tuple to the next n-tuple."""

        self.i += 1
        j = 0
        carry = 1
        while j < self.n and carry == 1 :
            if self.current[j] == self.limit[j] - 1 :
                self.current[j] = 0
                carry = 1
            else :
                self.current[j] += 1
                carry = 0
            j += 1

    def TupleToIndex(self, tuple) :
        return self.tupleConverter.TupleToIndex(tuple)

    def IndexToTuple(self, v) :
        return self.tupleConverter.IndexToTuple(v)

# Test:

if __name__ == '__main__' :
    a = NTupleGenerator([3,4,2])
    N = a.Num()
    for i in xrange(0,N) :
        v = a.TupleToIndex( a.Current() )
        r = a.IndexToTuple( v )
        print i, a.Current(), v, r
        a.Next()
