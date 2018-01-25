#!/usr/bin/python

import math, sys

## define Boltzmann constant (in kcal/mol)
kb=1.9858775e-3

class pmfWindow:

    def __init__(self,pmffile):


        """
        Initialise data for PMF window
        """
        
        ## store file name
        self.fname=pmffile

        ## open file containing probability data
        dataF=open(pmffile,'r')
        lines=dataF.readlines()

        ## get no of bins
        self.nbin=len(lines)-1

        ## read in k and x0
        data=lines[0].split()
        self.k=float(data[3])
        self.x0=float(data[6])

        # initialise probablilty and weight function dictionaries
        self.prob={}
        self.weight={}
        s=0.0
        for i,line in enumerate(lines[1:]):

            [r,p]=[float(d) for d in line.split()]
            tag=str(r)
            self.prob[tag]=p
            self.weight[tag]=0.5*self.k*(r-self.x0)**2
            s+=p
            if i==0:
                self.rmin=r
            else:
                self.rmax=r
            if i==1:
                self.dr=r-self.rmin
                


        ## normalise
        for k in self.prob.keys():
            self.prob[k]=self.prob[k]/s
        

        ## set initial offset
        self.off=0.0


def WhamCalcP(PMFWindows):

    """
    Calculate global P array for set of windows
    Uses constant offset for each window
    """

    ## initialise probability distribution
    p1={}
    p2={}
    p={}
    for win in PMFWindows:
        for k in win.prob.keys():

            if k in p1:
                p1[k]+=win.prob[k]
            else:
                p1[k]=win.prob[k]

        for k in win.weight.keys():
            
            if k in p2:
                s=win.off-win.weight[k]
                p2[k]+=math.exp(beta*s)
            else:
                s=win.off-win.weight[k]
                p2[k]=math.exp(beta*s)
                
    
    for k in p1.keys():
        p[k]=p1[k]/p2[k]

    return p
                

def WhamCalcF(PMFWindows,p):

    """
    Calculates offsets for PMF windows
    """

    ## initialise offsets for each window
    for win in PMFWindows:
        win.off=0
    
    ## loop over bins
    for r in p:
        for win in PMFWindows:
            if r in win.prob:
                win.off+=p[r]*math.exp(-beta*win.weight[r])

    ## take logs
    for win in PMFWindows:
        win.off=-kt*math.log(win.off)

    return

if __name__=='__main__':

    ## get arguments from command line

    ## first check for number of agruments
    if len(sys.argv) >= 4:

        ## get tolerance and max iterations off end of argument list
        tol=float(sys.argv.pop())
        maxit=int(sys.argv.pop())
        kt=kb*float(sys.argv.pop())
        outFile=sys.argv.pop()
        beta=1.0/kt
        
        ## get no of input files
        nfile=len(sys.argv[1:])

        ## initialise list of pmf data
        PMFWindows=[]

        ## read in data for each window
        for f in sys.argv[1:]:

            print "reading data from file ",f
            win=pmfWindow(f)
            PMFWindows.append(win)
            print len(win.prob)

        
        ## create global array
        p=WhamCalcP(PMFWindows)
    
        ## calculate offsets
        WhamCalcF(PMFWindows,p)
        for win in PMFWindows:
            print win.rmin,win.rmax,win.off

        ## loop over iterations
        ## (NB added one on to maxit, because I think in Fortran.....
        ## 0 based arrays, pah......)
        for it in range(0,maxit+1):

            ## print progress
            if it % 100==0:
                print 'iteration ',it,

            ## copy global P
            p_old=p

            

            ## calculate new P
            p=WhamCalcP(PMFWindows)
            k=p.keys()
            k.sort()
            ## find largest difference betwen old and new log(P)
            max_diff=0.0
            for r in p:
                if p[r]==0.0 or p_old[r]==0.0:
                    continue
                diff=(math.log(p[r])-math.log(p_old[r]))**2
                if diff > max_diff:
                    max_diff=diff

            ## print to screen
            if it % 100 ==0:
                print ' max diff = ',max_diff,

            # if converged exit
            if max_diff < tol:
                print 'max diff < tol; complete'
                break

            ## update off sets
            WhamCalcF(PMFWindows,p)
            if it % 100 ==0:
                print 'window offsets = ',
                for win in PMFWindows:
                    print win.off,

                print

        else:

            print 'max iterations exceeded'


        ## print final global P to file
        ofile=open(outFile,'w')

        k=[]
        for kk in p.keys():
            k.append(float(kk))
        k.sort()

        for kk in k:
            if p[str(kk)]>0.0:
                print >> ofile,"%f  %g %g "  % (kk,-kt*math.log(p[str(kk)]),p[str(kk)])
        
        
    else:

        print "Usage: wham.py <nfiles> <file1> <file2> ... <file_nfiles> <max iterations> <tolerance>"
