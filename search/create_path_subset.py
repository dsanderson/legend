import os, sys, random

def import_fnames():
    f = open('filenames.txt-full','r')
    names = f.read().strip().split('\n')
    f.close()
    return names

def export_fnames(names):
    f = open('filenames.txt','w')
    f.write('\n'.join(names))
    f.close()

#load up all the paths
random.seed(100)
names = import_fnames()
#get a subset of names
sub_names = random.sample(names,500)
export_fnames(sub_names)
