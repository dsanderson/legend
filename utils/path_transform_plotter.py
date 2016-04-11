import os, sys
import matplotlib.pyplot as plt

f = open('paths.out','r')
r = f.read()
f.close()

ls = r.split('\n')
#print len(ls)

p1 = []
p2 = []
p3 = []

state = None

for l in ls:
    #print l.strip() == 'Path 1:'
    if state == 'p3':
        if l.strip() == '':
            state = 'done'
        else:
            p3.append(tuple([float(i) for i in l.strip().split(',')]))
    if state == 'p2':
        if l.strip() == 'Path 1 transformed:':
            state = 'p3'
        else:
            p2.append(tuple([float(i) for i in l.strip().split(',')]))
    if state == 'p1':
        if l.strip() == 'Path 2:':
            state = 'p2'
        else:
            p1.append(tuple([float(i) for i in l.strip().split(',')]))
    if state == None:
        if l.strip() == 'Path 1:':
            #print 'entering p1'
            state = 'p1'

def path_to_xy(path):
    x = []
    y = []
    for p in path:
        x.append(p[0])
        y.append(p[1])
    return x,y

#print p3

plt.figure()
p1x,p1y = path_to_xy(p1)
plt.plot(p1x,p1y,'-r')
plt.hold(True)
p2x,p2y = path_to_xy(p2)
plt.plot(p2x,p2y,'-b')
p3x,p3y = path_to_xy(p3)
#print len(p3x)
plt.plot(p3x,p3y,'og')
plt.show()
