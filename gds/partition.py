#
# This file is a part of the GDS python library named gds. Copyright,
# Henning S. Mortveit 2015.
#

import sys
import copy
import itertools

if __name__ == '__main__' :
    sys.path += ["/Users/henning/git/gds"]

import equivalence
import networkx as nx

def ConvertGrowthString(s, labelList, n) :

    nBlocks = max( s ) + 1
    P = []
    for i in range(0, nBlocks) :
        P.append( [] )
    for i in range(0, n) :
        index = s[i]
        value = labelList[i]
        P[ s[i] ].append( labelList[i] )
        
    return P


def GenerateRestrictedGrowthStrings(n) :
    """Generates all the restricted growth strings as outlined in Knuth:
    The art of computer programming, pre-fascicle 3b, page 94.
    
    George Hutchinson, CACM 6:613-614, 1963.
    """

    P = []

    a = (n) * [0]
    b = (n) * [1]

    m = 1

    while True :

        # H2

        P.append( copy.deepcopy(a) )
        
        if a[n-1] == m :
            # H4
            j = n - 2
            while a[j] == b[j] :
                j -= 1
            # H5
            if j == 0 :
                return P
            else :
                a[j] += 1

            # H6
            m = b[j]
            if a[j] == b[j] :
                m += 1
            j += 1

            while j < n - 1 :
                a[j] = 0
                b[j] = m
                j += 1

            a[n-1] = 0

        else :
            # H3
            a[n-1] += 1

    return P


def IsReducible(G, block) :

    if len(block) <= 1 :
        return False
        
    if len(block) == 2 :
        if G.has_edge( block[0], block[1] ) :
            return False
        else :
            return True

    if nx.is_connected( G.subgraph( block ) ) :
        return False
    else :
        return True



def IsIrreducible(G, seq) :

    for block in seq :
        if IsReducible(G, block) :
            return False

    return True



def GenerateIrreducibleBlockSequences(G) :
    """Generates all the indecomposable unordered partitions of V(G)
    through growth strings as outlined in Knuth: The art of computer
    programming, pre-fascicle 3b, page 94.
    
    George Hutchinson, CACM 6:613-614, 1963.

    """

    P = []
    n = nx.number_of_nodes(G)

    a = (n) * [0]
    b = (n) * [1]

    m = 1

    labelList = range(0, n)

    while True :

        # H2

        seq = ConvertGrowthString(a, labelList, n)

        if IsIrreducible(G, seq) :
            P.append( seq )
        
        if a[n-1] == m :
            # H4
            j = n - 2
            while a[j] == b[j] :
                j -= 1
            # H5
            if j == 0 :
                return P
            else :
                a[j] += 1

            # H6
            m = b[j]
            if a[j] == b[j] :
                m += 1
            j += 1

            while j < n - 1 :
                a[j] = 0
                b[j] = m
                j += 1

            a[n-1] = 0

        else :
            # H3
            a[n-1] += 1

    return P


def GenerateBlockSequenceRepresentatives(G) :
    """Synopsis:

    For the graph G, this function does the following:

    1. Generates all indecomposable partitions of V(G), denoted by P.

    2. For each partition p of P, it generates the graph G \ p and its
    update sequence representatives translated back to the blocks of p.

    3. It returns a double list where each element is the list of
    representatives for G \ p as p varies over P. This list can be
    flatten as in the example contained at the end of this file.

    The function assumes that the vertices are labeled 0, 1, ...,
    n-1. The collection returned is canonical in the sense that each
    representative has a maximal number of blocks. Some blocks may be
    combined, but this will generally not lead to a canonical set of
    representatives.

    """

    partitionCollection = GenerateIrreducibleBlockSequences(G)

    globalCollection = []

    for partition in partitionCollection :

        # print "Partition: ", partition

        # Generate G \ partition with vertex set range(0, len(partition) )

        gMod = nx.blockmodel(G, partition)
        # print "Gmod - vertices: ", gMod.number_of_nodes()

        # Generate update sequence transversal

        linExt = equivalence.LinearExtensions( gMod )

        # print "Linear extensions: ", len(linExt)
        # for e in linExt :
        #     print "\t", e

        # Generate corresponding block sequences for this partition
        
        blockSequenceCollection = []

        for gModSeq in linExt :
            blockSequence = []
            for index in gModSeq :
                blockSequence.append( partition[index] )

            blockSequenceCollection.append( blockSequence )

        globalCollection.append( blockSequenceCollection )


    return globalCollection


def GenerateBlocks( growthStrings, labelList ) :

    B = []

    if len( growthStrings ) == 0 :
        return B
    
    else :
        n = len( growthStrings[0] )


    for s in growthStrings :
        P = ConvertGrowthString(s, labelList)
        B.append( copy.deepcopy( P ) )

    return B


if __name__ == '__main__' :

##

# n = 4

# P = GenerateRestrictedGrowthStrings(n)
# B = GenerateBlocks(P, range(0,n) ) # [1,2,3,4] 

# for s in B :
#     print s

# G = nx.path_graph(n)
# G.add_edge(0, n-1)
# B = GenerateIrreducibleBlockSequences(G)
# print ""
# for s in B :
#     print s

    G = nx.path_graph(3)
    T = GenerateBlockSequenceRepresentatives(G)

    print "# Block sequence representatives for Path(3):"
    for l in T :
        print l

    reps = itertools.chain.from_iterable(T)
    print "Reps: ", len(reps)
    for seq in reps :
        print "\t", seq
