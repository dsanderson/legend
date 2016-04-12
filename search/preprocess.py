import os, sys, subprocess, collections, time, copy
import random
import tqdm

Transform = collections.namedtuple("Transform",['tx','ty','rotation','scale'])

#####
# This file will preprocess the existing linkages,
#####
def path_to_xy(path):
    x = []
    y = []
    for p in path:
        x.append(p[0])
        y.append(p[1])
    return x,y

def import_fnames():
    f = open('filenames.txt','r')
    names = f.read().strip().split('\n')
    f.close()
    return names

def export_path(f_name, path):
    f = open(f_name,'w')
    f.write('x,y\n')
    for i in xrange(len(path[0])):
        f.write('{},{}\n'.format(path[0][i],path[1][i]))
    f.close()

def optimize_path(path_filename_1, path_filename_target):
    """Find an optimial transform for path 1 to minimize distance to path target"""
    command = ["./score.exe","--optimize",path_filename_1,path_filename_target]
    output = subprocess.check_output(command)
    #convert output to transform
    out_l = output.strip().split('\n')
    out_data = [l.split(':')[1] for l in out_l]
    out_data = [float(d) for d in out_data]
    t = Transform(tx = out_data[0], ty = out_data[1], rotation = out_data[2], scale = out_data[3])
    score = out_data[4]
    return score, t

def transform_path(t, path_filename):
    command = ["./score.exe","--transform",path_filename,str(t.tx),str(t.ty),str(t.rotation),str(t.scale)]
    output = subprocess.check_output(command)
    output = output.strip()
    xs = []
    ys = []
    for line in output.split('\n'):
        x = float(line.strip().split(',')[0])
        y = float(line.strip().split(',')[1])
        xs.append(x)
        ys.append(y)
    return xs,ys

#def select_path(db):

def canonicalize_path(path, target_path):
    f_name = os.path.basename(path)
    path_out = os.path.join("search","out",f_name)
    score, t = optimize_path(path, target_path)
    p2x,p2y = transform_path(t,path)
    export_path(path_out, [p2x,p2y])
    return path_out

def process_path(target_fname, fnames):
    scores = []
    for fname in tqdm.tqdm(fnames):
        score, t = optimize_path(fname, target_fname)
        scores.append(score)
    return scores

def write_db(name, scores, runID):
    f = open(os.path.join("search","out","db{}.txt".format(runID)),'a')
    f.write(':'+name+'\n')
    f.write(','.join([str(i) for i in scores])+'\n\n')
    f.close()

def main():
    t_num = 50
    runID = time.ctime()
    f = open(os.path.join("search","out","db-{}.txt".format(runID)),'w')
    f.close()
    fnames = import_fnames()
    fnames.sort()
    random.seed(100)
    #pick a name at random to start
    fname = random.choice(fnames)
    fname_orig = copy.deepcopy(fname)
    print "Processing {}".format(fname)
    scores = process_path(fname, fnames)
    for i in xrange(0,t_num):
        fname_new = random.choice(fnames)
        fname = canonicalize_path(fname_new, fname_orig)
        print "Processing {}".format(fname)
        scores = process_path(fname, fnames)
        write_db(fname, scores, runID)

if __name__ == '__main__':
    main()
