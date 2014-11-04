try:
    import cPickle as pickle
except:
    import pickle

def LoadObject(filename) :
    f = file(filename, 'r')
    u = pickle.Unpickler(f)
    o = u.load()
    f.close()  
    return o;

def DumpObject(filename,obj) :
    f = open(filename, 'w')
    u = pickle.Pickler(f)
    u.dump(obj)
    f.close()
    return 0;

