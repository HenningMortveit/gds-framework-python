#
#
#

import copy
import networkx

class SequenceError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "SequenceError"

class Word :
    def __init__(self, a) :
        if isinstance(a, list) :
            self.w = a
        elif isinstance(a, Word) :
            self.w = copy.deepcopy(a.w)
        elif isinstance(a, int) :
            self.w = list(a * [0])
        else :
            print "Type: ", type(a)
            raise SequenceError()


    def __repr__(self) :
        return str(self.w)

    def __str__(self) :
        return self.w.__str__()

    def __len__(self) :
        return len(self.w)

    def __setitem__(self, idx, v) :
        self.w[idx] = v

    def __getitem__(self, idx) :
        return self.w[idx]

    def append(self, v) :
        self.w.append(v)


class Permutation(Word) :
    def __init__(self, v) :
        Word.__init__(self, v)
        if isinstance(v, Permutation) :
            pass
        elif isinstance(v, list) : # trust the user...
            pass
        else :
            l = len(self.w)
            self.w = range(0,l)

    def append(self, v) :
        print "Cannot append to permutation."
        raise SequenceError()

    def __mul__(self, p) :
        prod = []
        for i, v in enumerate(p) :
            prod.append( self.w[v] )
        return Permutation(prod)

    def __invert__(self) :
        prod = len(self)*[0]
        for i, v in enumerate(self) :
            prod[v] = i
        return Permutation(prod)

class PermutationOrder :

    def __init__(self, p) :
        if not isinstance(p, Permutation) :
            print "Need to initialize PermutationOrder with Permutation!"
            raise SequenceError()

        self.p = ~p

    def LessThan(self, i, j) :
        return self.p[i] < self.p[j]


#networkx.is_directed_acyclic_graph

#    def __init__(self, acycO) :
#        pass


#   template <typename G>
#   unsigned int
#   AcyclicOrientation<G>::CanonicalPermutation(Permutation<vertex_t>& p) const
#   {
#     std::vector<Edge> edgeVec(edge);
#     std::vector<vertex_t> v;
#     std::vector<vertex_t> remaining(nVertices);

#     for(unsigned int i=0; i<nVertices; ++i)
#       remaining[i] = i;

#     while( 1 ){
#       const size_t nRemaining = remaining.size();
#       if( nRemaining == 0 )
# 	break;

#       std::vector<vertex_t> initialVec(0);

#       for(typename std::vector<vertex_t>::iterator i=remaining.begin();
# 	  i != remaining.end(); ++i)
# 	if( IsInitial(*i, edgeVec) )
# 	  initialVec.push_back(*i);

#       if( initialVec.empty() && nRemaining > 0 ){
# 	//std::cerr << "This is not an acyclic orientation." << std::endl;
# 	//p = Permutation<vertex_t> (0);
# 	return 1;
#       }

#       // delete initials from remaining

#       const size_t nInitial = initialVec.size();

#       for( unsigned int i=0; i<nInitial; ++i){
# 	remaining.erase(remove(remaining.begin(),
# 			       remaining.end(), initialVec[i]),
# 			remaining.end());
# 	RemoveEdgePredicate pred(initialVec[i]);
# 	edgeVec.erase(remove_if(edgeVec.begin(), edgeVec.end(),
# 				RemoveEdgePredicate (initialVec[i])),
# 		      edgeVec.end());
#       }

#       v.insert(v.end(), initialVec.begin(), initialVec.end());

#       //	copy(v.begin(), v.end(), ostream_iterator<int>(cout, " "));
#       //	cout << endl;
#     }

#     p = Permutation<vertex_t> (&v[0], nVertices);

#     return 0;
#   }


if __name__ == '__main__' :
    a = Word(5)
    print a

    a = Word([1, 2, 3])
    print a

    b = Word(a)
    b.append(4)
    print b

    a[1] = 2
    print a[1] == 2
    print a

    p = Permutation([0,2,1,3])
    q = Permutation([1,2,0,3])

    print isinstance(p, Word)
    print isinstance(p, Permutation)

    print p, "*", q, "=", p*q
    print q, "^-1 = ", ~q
    print p*~p

    pi_order = PermutationOrder(p)
    print p, pi_order.LessThan(3, 1)
