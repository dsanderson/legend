import os, sys, time
import itertools
import subprocess
import numpy as np
import tqdm

def parse_outfile():
    f = open('paths.out','r')
    r = f.read()
    f.close()
    l = r.split('\n')
    datum = float(l[1].split(':')[1].strip())
    return datum

def log_error(msg, runID):
    f = open('out/errors-{}.log'.format(runID),'a')
    f.write(msg)
    f.write('\n')
    f.close()

runID = time.ctime()

f = open('filenames.txt','r')
r = f.read()
f.close()
r = r.strip()
l = r.split('\n')
n_paths = len(l)

print "Found {} paths.".format(n_paths)

indecies = range(0,n_paths)
index_pairs = itertools.permutations(indecies,2)
index_pairs = list(index_pairs)
print "{} total pairs to check.".format(len(index_pairs))

dists = np.zeros((n_paths,n_paths))
previous_dist = None #used to check that the program ran successfully

for i in tqdm.tqdm(index_pairs):
    try:
        command = './a.out {} {} > paths.out'.format(i[0],i[1])
        subprocess.call(command, shell=True)
        dist = parse_outfile()
        if dist == previous_dist:
            log_error('Error when processing indecies {} and {}'.format(i[0], i[1]),runID)
        else:
            dists[i[0],i[1]] = dist
        previous_dist = dist
    except:
        log_error('Error when processing indecies {} and {}'.format(i[0], i[1]),runID)
np.savetxt('out/dists-{}.mat'.format(runID),dists)
print "\nRun Complete!\n"
