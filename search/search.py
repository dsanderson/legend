import os, sys, copy
import preprocess
import matplotlib.pyplot as plt

def import_fnames():
    f = open('filenames.txt','r')
    names = f.read().strip().split('\n')
    f.close()
    return names

def import_db(db_path = 'search/out/dbMon Apr 11 23:29:35 2016.txt'):#'search/out/dbMon Apr 11 20:43:00 2016.txt'):
    f = open(db_path,'r')
    r = f.read()
    f.close()
    lines = r.split('\n')
    db = {}
    for i,l in enumerate(lines):
        if l!='' and l[0]==':':
            name = l[1:].strip()
            data = lines[i+1].strip().split(',')
            data = [float(d) for d in data]
            db[name] = copy.deepcopy(data)
    return db

def path_to_xy(path):
    x = []
    y = []
    for p in path:
        x.append(p[0])
        y.append(p[1])
    return x,y

def import_path(fname):
    f = open(fname,'r')
    r = f.read().strip()
    f.close()
    lines = r.split('\n')
    path = []
    for l in lines[1:]:
        x = float(l.split(',')[0])
        y = float(l.split(',')[1])
        path.append((x,y))
    return path

def search(path, db):
    names = db.keys()
    names.sort()
    dists = [-1]*len(db[names[0]])
    for n in names:
        #get the distance
        dist_n, t = preprocess.optimize_path(path,n)
        print dist_n
        #maintain the largest gap between desired score and actual score
        for i,s in enumerate(db[n]):
            if abs(s-dist_n)>dists[i]:
                dists[i] = abs(s-dist_n)
    #get the item with the smallest band
    min_index,min_value = min(enumerate(dists), key = lambda p:p[1])
    return min_index, min_value

def main():
    fnames = import_fnames()
    fnames.sort()
    db = import_db()
    path = "search/tmp/0.csv"
    min_i, min_s = search(path, db)
    print min_s
    #now minimize the target path, and print that score
    dist_n, t = preprocess.optimize_path(path,fnames[min_i])
    print dist_n
    xs1,ys1 = preprocess.transform_path(t,path)
    xs2,ys2 = path_to_xy(import_path(fnames[min_i]))
    plt.plot(xs1,ys1,'r')
    plt.hold(True)
    plt.plot(xs2,ys2,'g')
    plt.show()

if __name__ == '__main__':
    main()
