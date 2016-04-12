from __future__ import division
import os, sys, math

def export_path(f_name, path):
    f = open(f_name,'w')
    f.write('x,y\n')
    for i in xrange(len(path)):
        f.write('{},{}\n'.format(path[i][0],path[i][1]))
    f.close()

if __name__ == '__main__':
    #make a circle
    l = 60
    pts = range(0,60)
    pts = [(p/l)*2*math.pi for p in pts]
    c_pts = [(math.cos(p)/2,math.sin(p)/2) for p in pts]
    fname = 'search/tmp/0.csv'
    export_path(fname,c_pts)
