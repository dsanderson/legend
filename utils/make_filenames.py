# Program to create the filenames.txt file from all path files in the usual directory
import os, sys, glob

#get list of all .csv files
paths = glob.glob('./paths/data/*_path.csv')
print 'Found {} paths.'.format(len(paths))

paths.sort()

f = open('filenames.txt','w')
for path in paths:
    f.write(path)
    f.write('\n')
f.close()
