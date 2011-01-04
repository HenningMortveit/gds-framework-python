#
#
#

import sequence

def ExpandGroup( permutations ) :
    """Here permutations is a python set of consisting of group
    generators."""

    newSet = set()

    for p1 in permutations :
        for p2 in permutations :
            newSet.add( p1*p2 )

    permutations.update( newSet )


def ComputeGroup( permutationGenerators ) :
    """Compute the group with permutation generators as given. Of
    course, it is assumed that the group is finite and sufficiently
    small. It is probably a better idea to use Sage for this kind of
    computation."""

    genSet = set( permutationGenerators )

    n0 = len(genSet)
    ExpandGroup(genSet)
    n1 = len(genSet)

    while n1 > n0 :
#        print n0, n1
#        print genSet
        n0 = n1
        ExpandGroup(genSet)
        n1 = len(genSet)

    return list(genSet)



def CreateAutQ2_3() :
    """ """

    p1 = sequence.Permutation( [1, 3, 0, 2, 5, 7, 4, 6] )
    p2 = sequence.Permutation( [4, 5, 0, 1, 6, 7, 2, 3] )
    p3 = sequence.Permutation( [4, 5, 6, 7, 0, 1, 2, 3] )

    return ComputeGroup( [p1, p2, p3] )


def C_n( n ) :
    """ """

    sigma = sequence.Permutation(n)
    for i in range(0,n) :
        sigma[i] = (i + 1) % n

    return ComputeGroup( [sigma] )


def D_n(n) :
    """ """

    sigma = sequence.Permutation(n)
    tau = sequence.Permutation(n)

    for i in range(0,n) :
        sigma[i] = (i + 1) % n
        tau[i] = n - 1 - i;

    return ComputeGroup( [sigma, tau] )
