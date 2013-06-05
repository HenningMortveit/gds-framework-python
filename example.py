
#import pygraphviz as pgv

import gds.util.enumeration
import gds.state
import gds.graphs
import gds.functions
import gds.gds
import gds.algorithms
import gds.state_algorithms
import gds.phase_space
import gds.sequence
import gds.equivalence
import gds.orientation
import gds.groups
import gds.sequence


# from matplotlib import rc
# #rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# ## for Palatino and other serif fonts use:
# #rc('font',**{'family':'serif','serif':['Palatino']})
# rc('text', usetex=True)
# rc('font', family='serif')
# rc('font', size=10 )


import networkx as nx
from networkx.algorithms import *

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import MaxNLocator

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_pdf import PdfPages

try:
    import cPickle as pickle
except:
    import pickle

import threading
import multiprocessing
import thread
import math
import copy
import sys
import cProfile
import numpy

def LoadObject(filename) :
    f = file(filename, 'r')
    u = pickle.Unpickler(f)
    o = u.load()
    f.close()  # AA: this was not there before
    return o;

# ------------------------------------------------------------
# AA: opposite of LoadObject

def DumpObject(filename,obj) :
    f = open(filename, 'w')
    u = pickle.Pickler(f)
    u.dump(obj)
    f.close()
    return 0;



def PlotExample() :
    X = networkx.Graph()
    X.add_edge( 0, 1);
    X.add_edge( 0, 2);
    X.add_edge( 1, 2);

    pos = dict();
    pos[0] = [0,0]
    pos[1] = [1,0]
    pos[2] = [1,1]

    networkx.drawing.nx_pylab.draw_networkx(X, pos=pos)
    plt.show()

def MakePNASNetwork() :
    X = networkx.Graph()
    edges = [
        (1,2), (1,3),
        (2,8), (2,10),
        (3,4), (3,10),
        (4,5), (4,9),
        (5,7), (5,8), (5,10),
        (6,7), (6,9), (6,10), (6,11),
        (7,8), (7,9), (7,10), (7,11),
        (8,9), (8,10), (8,11),
        (9,10),
        (10,11)
        ]
    for e in edges :
        X.add_edge(e[0], e[1])
    return X


def BiThresholdExample() :

    n = 4
    pi = [0,1,2,3];
    X = gds.graphs.CircleGraph(n)
    doCircle = True
#    X = gds.graphs.WheelGraph(n-1)
#    X = gds.graphs.HyperCube(dim = 3, base = 2)
    f = n * [gds.functions.biThreshold(1,3)]
#    one  = gds.state.State(1, 2)
#    zero = gds.state.State(0, 2)

#     s = [one,zero,zero]
#     i = [0,1,2]
#     print f[0](s,i,1)
#     sys.exit(0)

    stateObject = n * [gds.state.State(0, 2)]


    gds1 = gds.gds.GDS(X, f, stateObject, doCircle)
    gds1.SetSequence(pi)
#    gds1.SetParallel()


    transitions = gds.algorithms.GenerateTransitions(gds1)
    fixedPoints = gds.algorithms.FixedPoints(gds1, transitions)

    p = gds.phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: "
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

    print "Periodic points: "
    for i, cycle in enumerate(periodicPoints) :
        print i
        for j in cycle :
            print gds1.IntegerToState(j)

    print "Components: ", components

    for x,y in enumerate(transitions) :
        print gds1.IntegerToState(x), "->", gds1.IntegerToState(y)

    return transitions

def DynThresholdExample() :

    n = 5

    X = gds.graphs.StarGraph(n)
    stateObject = (n+1) * [gds.state.StateDynT(0, 1, 1)]
    stateObject[0] = gds.state.StateDynT(0,1, n)

    f = (n+1) * [gds.functions.f_up_down]

    gds1 = gds.gds.GDS(X, f, stateObject, False)

    transitions = gds.algorithms.GenerateTransitions(gds1)
    fixedPoints = gds.algorithms.FixedPoints(gds1, transitions)

    p = gds.phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: %i" % len(fixedPoints)
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

def SDSExample() :
    """Basic example for phase space on X = Circle_4."""

    n = 4

    pi0 = [3,2,1,0]

    pi1 = [0,1,2,3,4,5]
    pi2 = [0,1,5,2,3,4]
    pi3 = [0,1,5,2,4,3]
    pi4 = [0,1,5,4,3,2]
    pi5 = [0,5,4,3,2,1]

    X = gds.graphs.CircleGraph(n)
    #f = n * [gds.functions.wolfram(110)]
    #f = n * [gds.functions.nor]
    f = n * [gds.functions.wolfram(240)]

#    one  = gds.state.State(1, 2)
#    zero = gds.state.State(0, 2)

#     s = [one,zero,zero]
#     i = [0,1,2]
#     print f[0](s,i,1)
#     sys.exit(0)

    stateObject = n * [gds.state.State(0, 2)]

    doCircle = True
    gds1 = gds.gds.GDS(X, f, stateObject, doCircle)
    gds1.SetSequence(pi0)

    transitions = gds.algorithms.GenerateTransitions(gds1)
    fixedPoints = gds.algorithms.FixedPoints(gds1, transitions)

    p = gds.phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: "
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

    print "Periodic points: "
    for i, cycle in enumerate(periodicPoints) :
        print i
        for j in cycle :
            print gds1.IntegerToState(j)

    print "Components: ", components

    for x,y in enumerate(transitions) :
        print gds1.IntegerToState(x), "->", gds1.IntegerToState(y)

    return transitions



def SDSBlockSequenceExample() :
    """Basic example for phase space on X = Circle_4."""

    n = 5

    pi0 = [[0,3], [4], [1], [2]]

    X = gds.graphs.CircleGraph(n)
    f = n * [gds.functions.nor]

    stateObject = n * [gds.state.State(0, 2)]

    doCircle = True
    gds1 = gds.gds.GDS(X, f, stateObject, doCircle)
    gds1.SetBlockSequence(pi0)

    transitions = gds.algorithms.GenerateTransitions(gds1)
    fixedPoints = gds.algorithms.FixedPoints(gds1, transitions)

    p = gds.phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: "
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

    print "Periodic points: "
    for i, cycle in enumerate(periodicPoints) :
        print i
        for j in cycle :
            print gds1.IntegerToState(j)

    print "Components: ", components

    for x,y in enumerate(transitions) :
        print gds1.IntegerToState(x), "->", gds1.IntegerToState(y)

    return transitions



def SDSExample3() :
    """Basic example for phase space on X = Circle_4."""

    n = 3

    pi1 = [0,1,2]

    #X = gds.graphs.CircleGraph(n)


    X = networkx.Graph()
    X.add_edge( 0, 1);
    X.add_edge( 0, 2);
    X.add_edge( 1, 2);


    f = n * [gds.functions.nand]

    stateObject = n * [gds.state.State(0, 2)]

    doCircle = True
    gds1 = gds.gds.GDS(X, f, stateObject, doCircle)
#    gds1.SetSequence(pi2)

    transitions = gds.algorithms.GenerateTransitions(gds1)
    fixedPoints = gds.algorithms.FixedPoints(gds1, transitions)

    p = gds.phase_space.PhaseSpace(gds1)

    fixedPoints = p.GetFixedPoints()
    periodicPoints = p.GetPeriodicPoints()
    components = p.GetComponents()

    print "Fixed points: "
    for i in fixedPoints :
        print i, gds1.IntegerToState(i)

    print "Periodic points: "
    for i, cycle in enumerate(periodicPoints) :
        print i
        for j in cycle :
            print gds1.IntegerToState(j)

    print "Components: ", components

    for x,y in enumerate(transitions) :
        print gds1.IntegerToState(x), "->", gds1.IntegerToState(y)

    return transitions



def SDSExample2() :
    """Basic example for phase space on X = Circle_4."""

    n = 4
    circ = gds.graphs.CircleGraph(n)
    #f = n * [gds.functions.wolfram(110)]
    f = n * [gds.functions.majority]
    stateObject = n * [gds.state.State(0, 2)]

    gds1 = gds.gds.GDS(circ, f, stateObject, True)
    le = gds.equivalence.LinearExtensions( circ )

    s = list()

    for pi in le :
        gds1.SetSequence(pi)
        transitions = gds.algorithms.GenerateTransitions(gds1)
        if not transitions in s :
            s.append(transitions)

    print len(s)
#    p = gds.phase_space.PhaseSpace(gds1)





def NetworkXExample(transitions) :
    """Example of how phase space can be manipulated by network x"""

    d = nx.DiGraph()
    for i in range(0, len(transitions) ) :
        d.add_edge(i,transitions[i])

    orbits = attracting_components(d)
    print "Periodic orbits: ", orbits

    components =  weakly_connected_components(d)
    print "Components: ", components

    return d



#import itertools

#for p in itertools.chain(itertools.permutations([0,1,2,3])) :
#    print p

def OrientationExample() :
    circ =  gds.graphs.CircleGraph(4)
    pi = gds.sequence.Permutation([0,1,2,3])
    aO = gds.orientation.Orientation(graph = circ, permutation = pi)

    print "Orientation", "{3,2}", aO( (3,2) )
    print "Orientation", "{2,3}", aO( (2,3) )
    print "Linear extension: ", aO.LinearExtension()



def FinalExam() :
    n = 7

    X = networkx.Graph()
    edges = [
        [0,1], [0,3], [0,5],
        [1,2], [1,6],
        [3,2], [3,4], [0,5],
        [5,4], [5,6]
        ]
    for e in edges :
        X.add_edge(e[0], e[1])

    print "Linear extensions:"
    le = gds.equivalence.LinearExtensions( X )
    for e in le :
        print "\t", e

    print "\talpha(Y) = ", len(le)

    print "Kappa representatives - linear extensions:"
    kle = gds.equivalence.KappaLinearExtensions(X, 0)
    for e in kle :
        print "\t", e

    print "\tkappa(Y) = ", len(kle)


    p1 = gds.sequence.Permutation( [0, 3, 4, 5, 6, 1, 2] )
    p2 = gds.sequence.Permutation( [0, 3, 2, 1, 6, 5, 4] )

    autX = gds.groups.ComputeGroup( [p1, p2] )


    print "Kappa bar representatives - linear extensions:"
    kble = gds.equivalence.KappaBarClasses(X, autX)
    for e in kble :
        print "\t", e[1]

    print "\tkappabar(Y) = ", len(kble)


    k = gds.equivalence.EnumAlphaBarClasses(X, autX)
    print "\talphabar(X) = ", k


def PhaseSpace() :
    """Basic example for phase space on X = Circle_4."""

    n = 4
    circ = gds.graphs.CircleGraph(n)
    f = n * [gds.functions.majority]
    stateObject = n * [gds.state.State(0, 2)]

    gds1 = gds.gds.GDS(circ, f, stateObject, True)

    phaseSpace = gds.phase_space.PhaseSpace(gds1);
    components = phaseSpace.GetComponents()
    print components
    fixedPoints = phaseSpace.GetFixedPoints();
    print fixedPoints
    periodicPoints = phaseSpace.GetPeriodicPoints()
    print periodicPoints

def NotEqual(a,b) :
    return a!=b

def HammingDistance(x,y) :
    assert len(x) == len(y)
    return sum( map(NotEqual, x, y) )

def HammingNorm(x) :
    return HammingDistance(x, len(x)*[gds.state.State(0, 2)] )

def DerridaDiagram(gds1) :

#     n = 4
#     circ = gds.graphs.CircleGraph(n)
#     f = n * [gds.functions.nor]
#     stateObject = n * [gds.state.State(0, 2)]
#     gds1 = gds.gds.GDS(circ, f, stateObject, True)

    n = gds1.GetDim()

    phaseSpace = gds.phase_space.PhaseSpace(gds1);
    F = phaseSpace.GetTransitions()

    diagram = []
    for i in range(0, n+1) :
        diagram.append( (n+1)*[0] )

    n = gds1.GetDim();
    stateObjectList = gds1.stateObjectList
    limit = gds1.tupleConverter.limit
    ng = gds.util.enumeration.NTupleGenerator(limit)
    nStates = ng.Num()

    x = n*[0]
    y = n*[0]
    image_x = n*[0]
    image_y = n*[0]

    for i in xrange(0, nStates) :
        config = ng.Current()

        # Convert from index space to state space:
        for j in range(0,n) :
            x[j] = stateObjectList[j].IndexToState( config[j] )
        image_x =  gds1.tupleConverter.IndexToTuple( F[i] )

        ng2 = copy.deepcopy(ng)

#        print "x", x, image_x

        for j in xrange(i+1, nStates) :
            ng2.Next()
            config = ng2.Current()
            for k in range(0,n) :
                y[k] = stateObjectList[k].IndexToState( config[k] )

            hd = HammingDistance(x,y)
            image_y = ng.IndexToTuple( F[j] )
            hd2 = HammingDistance(image_x, image_y)
            diagram[hd][hd2] += 1
#            print x, y, image_x, image_y, hd, hd2

        ng.Next()

    return diagram


def ComputeGDSPhaseSpaceProps(gds1) :

    n = gds1.GetDim()

    phaseSpace = gds.phase_space.PhaseSpace(gds1);

    F = phaseSpace.GetTransitions()
    componentList = phaseSpace.GetComponents()
    attractorList = phaseSpace.GetPeriodicPoints()

    compID = len(F) * [-1]

    for componentID in range(0, len(componentList) ):
        for j in range(0, len(componentList[componentID]) ) :
            compID[ componentList[componentID][j] ] = componentID

    attractorToComponentMap = len(attractorList) * [-1]
    componentToAttractorMap = len(componentList) * [-1]

    j = 0
    for attractor in attractorList :
        attractorToComponentMap[j] = compID[ attractor[0] ]
        componentToAttractorMap[ compID[ attractor[0] ] ] = j
        j += 1

    return F, componentList, attractorList, compID, attractorToComponentMap, componentToAttractorMap


def AttractorMatrix(gds1) :
    n = gds1.GetDim()

    _, _, attractorList, compID, _, componentToAttractorMap = ComputeGDSPhaseSpaceProps(gds1)

    numAttractors = len(attractorList)

    attractorMatrix = []
    
    j = 0
    for attractor in attractorList :

        nStates = len(attractor)
        nPerturbations = n * nStates
        fraction = 1.0/float( nPerturbations )

        attractorMatrix.append( [0.0] * numAttractors )

        for stateIndex in attractor :
            state = gds1.IntegerToState(stateIndex)
            for i in range(0,n) :
                state[i].x = 0 if state[i].x == 1 else 1
                nborIndex = gds1.StateToInteger(state)
                state[i].x = 0 if state[i].x == 1 else 1
                attractorID = componentToAttractorMap[ compID[nborIndex] ]
                attractorMatrix[j][ attractorID ] += 1.0

        j += 1


    return attractorMatrix

def StateSensitivity(gds1) :

    """Computes:
    N1 - histogram of state sensitivity split by Hamming norm
    N2 - histogram of number of unique images in 1-neighborhood split by Hamming norm
    N3 - histogram of attractor sensitivity split by Hamming norm
    N4 - histogram of number of attractors in 1-neighborhood split by Hamming norm
    """

    F, _, _, compID, _, _ = ComputeGDSPhaseSpaceProps(gds1)

    n = gds1.GetDim()

    N1_diagram = []
    for i in range(0, n+1) :
        N1_diagram.append( (n+1)*[0] )

    N2_diagram = []
    for i in range(0, n+1) :
        N2_diagram.append( (n+2)*[0] )

    N3_diagram = []
    for i in range(0, n+1) :
        N3_diagram.append( (n+1)*[0] )

    N4_diagram = []
    for i in range(0, n+1) :
        N4_diagram.append( (n+2)*[0] )

    nStates = gds1.NumStates()

    for i in xrange(0, nStates) :

        x = gds1.IntegerToState(i)

        hn = HammingNorm(x)
        i_image = F[i]
        i_comp = compID[i]

        dist = 0
        n2_set = set()
        n2_set.add(i_image)
        comp_dist = 0
        n4_set = set()
        n4_set.add(i_comp)

        for j in xrange(0, n) :

            x[j].x = (x[j].x+1) % 2
            index = gds1.StateToInteger(x)
            x[j].x = (x[j].x+1) % 2

            j_image = F[index]
            n2_set.add(j_image)
            n4_set.add( compID[index] )

            if i_image != j_image :
                dist += 1
            if i_comp != compID[index] :
                comp_dist += 1

        N1_diagram[hn][dist] += 1
        N2_diagram[hn][ len(n2_set) ] += 1
        N3_diagram[hn][ comp_dist ] += 1
        N4_diagram[hn][ len(n4_set) ] += 1

#        print hn
#        print "N2:", n2_set
#        print "N4:", n4_set


    return N1_diagram, N2_diagram, N3_diagram, N4_diagram

def DiagTranspose(m) :
    nRows = len(m[0])
    nCols = len(m)
    M = []
    for i in range(0, nRows) :
        M.append( nCols*[0] )

    for i in range(0, nRows) :
        for j in range(0, nCols) :
            M[i][j] = m[j][i]

    return M

def ColumnNormalize(m) :
    M = copy.deepcopy(m)
    for i in range(0, len(M) ) :
        col = M[i]
        s = float( sum( col ) )
        if s == 0.0 :
            continue
        else :
            s = 1.0/s
            for j in range(0, len(col) ):
                col[j] *= s

    return M


def ComputeStats( v ) :
    n = sum(v)
    if n == 0 :
        return 0, 0
    avg = 0.0
    var = 0.0
    for i in range(0, len(v)) :
        avg += v[i]*i
        var += v[i]*i*i
    avg = avg/n
    var = (var - n*avg*avg)
    stdev = math.sqrt(var/n)
    return  avg, stdev

def ComputeAllStats( M ) :
    """Compute the average and standard deviation for each element of M"""

    s = []
    for i in range(0, len(M)) :
        s.append( [i, ComputeStats(M[i]) ] )

    x = []
    y = []
    yerr = []
    for v in s :
        x.append(v[0])
        y.append(v[1][0])
        yerr.append(v[1][1])

    return x, y, yerr

def AttractorMatrixStats(gds1) :

    t = 1

    A = AttractorMatrix(gds1)
    if len(A) == 0 :
        return 

    dim = len(A[0])
    g = nx.DiGraph()
    g.add_nodes_from( range(0, dim) )

    i = 0
    for row in A :
        for j in range(0,dim) :
            if A[i][j] >= t :
                g.add_edge(i, j)
        i += 1

    components = nx.algorithms.weakly_connected_components(g)
    print len(components), components


def AttractorMatrixList(gdsList) :
    j = 0
    for g in gdsList :
        print j
        AttractorMatrixStats(g)
        j += 1

def ComputeDiagrams(gdsList, indexList, diagrams) :
    for i in indexList :
        gds1 = gdsList[i]
        N1_diagram, N2_diagram, N3_diagram, N4_diagram = StateSensitivity(gds1)
        ddiag = DerridaDiagram(gds1)
        #diagrams[i] = [ddiag, N1_diagram, N2_diagram, N3_diagram, N4_diagram]
        DumpObject("%i.txt" % i, [ddiag, N1_diagram, N2_diagram, N3_diagram, N4_diagram])
        print "GDS<", i, "> done"



def ComputeStabilityArray(gdsList) :

    m = len(gdsList)
    diagrams = []
    for i in range(0,m) :
        diagrams.append( [] )

    processList = []
    for j in range(1, m+1) :
        t = multiprocessing.Process( target=ComputeDiagrams,
                                     args=( gdsList, [j-1], diagrams) )
        t.start()
        processList.append(t)

    for t in processList :
        t.join()

    # Collect the input:
    for i in range(0, m) :
        diagrams[i] = LoadObject("%i.txt" % i)

    return diagrams


def PlotStabilityArray(diagrams, density=True) :

    m = len(diagrams)

#    matplotlib.rcParams.update({'font.size': 10})
    name = 'plots-exp-stdev.pdf'
    if density == True :
        name = 'plots-density.pdf'

    pdf_pages = PdfPages(name)

    fig, axs = plt.subplots(nrows=m, ncols=5, sharex=True, sharey=True)
    plt.gray()

    t = [r"\noindent Derrida\\diagram",
         r"$s(x)/H(x)$ (v.1)",
         r"$s(x)/H(x)$ (v.2)",
         r"$\omega$-limit (v.1)",
         r"$\omega$-limit (v.2)"]

    t = ["1", "2", "3", "4", "5"]

    for j in range(0, m) :

        diags = diagrams[j]

        for i in range(0, len(diags)) :

            d = diags[i]
            ax = plt.subplot2grid((m,5),(j, i))
            if j == 0 :
                if density == True :
                    ax.set_title(t[i]) # fontsize=12)
                else :
                    ax.set_title(t[i]) # 'Exp/StDev') # , fontsize=12)

            if density == False :
                x, y, yerr = ComputeAllStats( d )
                ax.errorbar(x, y, yerr=yerr, fmt='o')

            else :
                im = ax.imshow(DiagTranspose( ColumnNormalize( d) ), origin="lower", interpolation="nearest")
                if i == len(diags) - 1 or i == 0:
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes("right", size="5%", pad=0.05)
                    if i == 0 :
                        cbar = plt.colorbar(im, cax=cax, ticks=[0, 0.25, 0.5, 0.75, 1.0])
                        cbar.ax.set_yticklabels([0, 0.25, 0.5, 0.75, 1.0])
                    else :
                        cbar = plt.colorbar(im, cax=cax, ticks=[0, 0.5, 1.0])
                        cbar.ax.set_yticklabels([0, 0.5, 1.0])




    plt.tight_layout()

#    plt.subplots_adjust(wspace = 0.65)
    pdf_pages.savefig(fig, bbox_inches='tight')
    pdf_pages.close()
    plt.show()



def main() :

    n =16
    r = 2

    m = int( math.ceil( float(n)/2 ) )

    gdsList = []

    for j in range(r, m+1) :

        circ = gds.graphs.GeneralCircleGraph(n,r)

        if j > r :
            circ.add_edge( 0, j )


#        f = n * [gds.functions.wolfram(1)]
        f = n * [gds.functions.biThreshold(2,4)]
        f = n * [gds.functions.parity]
#        f = n * [gds.functions.nor]
        stateObject = n * [gds.state.State(0, 2)]
        flag = (True) if j == 1 else False
        flag = False
        gds1 = gds.gds.GDS(circ, f, stateObject, flag)
        gds1.SetSequence(range(0,n))
        gdsList.append(gds1)




        # phaseSpace = gds.phase_space.PhaseSpace(gds1);
        # pp = phaseSpace.GetPeriodicPoints()
        # c = phaseSpace.GetComponents() 

        # sizes = [len(i) for i in pp]
        # s = sum(sizes)
        # print j, len(pp), s, pp #, sizes
        # print ""

    AttractorMatrixList(gdsList)
    #diagrams = ComputeStabilityArray(gdsList)
    #PlotStabilityArray(diagrams, density=True)
    #PlotStabilityArray(diagrams, density=False)
    sys.exit(-1)


    n = 10
    circ = gds.graphs.CircleGraph(n)
#    circ.add_edge( 0, 5 )
#    circ.add_edge( 2, 7 )

    f = n * [gds.functions.wolfram(150)]
#    f = n * [gds.functions.nor]
    stateObject = n * [gds.state.State(0, 2)]
    gds1 = gds.gds.GDS(circ, f, stateObject, True)
#    gds1.SetSequence(range(0,n))


    N1_diagram, N2_diagram, N3_diagram, N4_diagram = StateSensitivity(gds1)
    ddiag = DerridaDiagram(gds1)

    print "N1:", N1_diagram
    print "N2:", N2_diagram
    print "N3:", N3_diagram
    print "N4:", N4_diagram
    print "DD:", ddiag

    k = 0

    for d in [N1_diagram, N2_diagram, N3_diagram, N4_diagram, ddiag] :

        fig, axs = plt.subplots(nrows=1, ncols=2, sharex=False)
        print "figure:", fig

        ax = axs[0]
        x, y, yerr = ComputeAllStats( d )
        ax.errorbar(x, y, yerr=yerr, fmt='o')
        ax.set_title('Exp/StDev', fontsize=12)

        ax = axs[1]
        plt.gray()
        im = ax.imshow( DiagTranspose( ColumnNormalize( d) ), origin="lower", interpolation="nearest")
        fig.colorbar(im)

        ax.set_title(k+1, fontsize=12)



        k+=1


        #    plt.colorbar()
        #    plt.show()


    matplotlib.rcParams.update({'font.size': 12})
    pdf_pages = PdfPages('plots.pdf')

    fig, axs = plt.subplots(nrows=1, ncols=5, sharex=True, sharey=True)


    diags = [ddiag, N1_diagram, N2_diagram, N3_diagram, N4_diagram]

    k = 1
    im = 0
    for i in range(0, len(diags)) :

        d = diags[i]
        ax = plt.subplot(150+k)
        ax.set_title(k, fontsize=12)

        im = ax.imshow(DiagTranspose( ColumnNormalize( d) ), origin="lower", interpolation="nearest")


        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im, cax=cax)


#        plt.gca().xaxis.set_major_locator( MaxNLocator(nbins = 7, prune = 'lower') )
        plt.gca().yaxis.set_major_locator( MaxNLocator(nbins = 6) )
        cbar.locator = MaxNLocator( nbins = 6)


#        plt.colorbar(im)
        plt.gray()

        k+=1

    #plt.tight_layout()

    plt.subplots_adjust(wspace = 0.65)
    pdf_pages.savefig(fig, bbox_inches='tight')
    pdf_pages.close()
    plt.show()



    sys.exit(0);



    DynThresholdExample()
    sys.exit(0)

    BiThresholdExample()
    sys.exit(0)



    SDSBlockSequenceExample()
    sys.exit(0)

    FinalExam();
    sys.exit(0);

    SDSExample3()
    sys.exit(0)


    SDSExample()
    sys.exit(0)


    X = MakePNASNetwork()
    X = gds.graphs.PathGraph(4)
    print X.edges()

    le = gds.equivalence.LinearExtensions( X )
    print len(le)
    for pi in le :
        print "\t", pi


    sys.exit(0)
    SDSExample2()

    transitions = SDSExample()
    NetworkXExample(transitions)
    OrientationExample()

    circ = gds.graphs.PathGraph(6)
    circ = gds.graphs.WheelGraph(4)
    q23 = gds.graphs.HyperCube(dim = 3, base = 2)
    circ = gds.graphs.CircleGraph(4)

    print "Circle:"
    print "\tVertices:", circ.nodes()
    print "\tEdges:", circ.edges()


    # Circle case

    n = 4

    c = gds.graphs.CircleGraph(n)
    d = gds.groups.D_n(n)

    print "circle graph:", n
    print "Linear extensions:"
    le = gds.equivalence.LinearExtensions( c )
    for e in le :
        print "\t", e

    print "Kappa representatives - linear extensions:"
    kle = gds.equivalence.KappaLinearExtensions(c, 0)
    for e in kle :
        print "\t", e

    print "Kappa bar representatives - linear extensions:"
    kble = gds.equivalence.KappaBarClasses(c, d)
    for e in kble :
        print "\t", e[1]

    print "Circle", n
    print "\talpha(Y) = ", len(le)
    print "\tkappa(Y) = ", len(kle)
    print "\tkappabar(Y) = ", len(kble)
    print ""

    # 3-cube

    q23 = gds.graphs.HyperCube(dim = 3, base = 2)
    autq23 = gds.groups.CreateAutQ2_3()

    le = gds.equivalence.LinearExtensions( q23 )
    for e in le :
        print "\t", e

    print "Kappa representatives - linear extensions:"
    kle = gds.equivalence.KappaLinearExtensions(q23, 0)
    for e in kle :
        print "\t", e

    print "Kappa bar representatives - linear extensions:"
    kble = gds.equivalence.KappaBarClasses(q23, autq23)
    for e in kble :
        print "\t", e[1]

    print "3-cube", n
    print "\talpha(Y) = ", len(le)
    print "\tkappa(Y) = ", len(kle)
    print "\tkappabar(Y) = ", len(kble)
    print ""

    #networkx.draw(q23)
    networkx.draw_graphviz(q23)
# ------------------------------------------------------------

if __name__ == "__main__":
    main()

#cProfile.run('main()', 'profile.txt')
