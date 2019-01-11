import numpy as np

################################################################
# This is the file that checks the overlap of the real samples #
################################################################

nSamples      = 74
nChromes      = 12

trueSampleLoc = np.loadtxt('trueSampleLength.txt')
#y2            = np.loadtxt('chromeLength.txt')
#sampleLen     = y1[:,1]
#trueSampleLoc   = y1[:,2]
##sampleStart   = y1[:,3] 
#chromeLen     = y2[:,1]


RED   = 0
GREEN = 1
BLUE  = 2

RR = 0
GG = 1
BB = 2
RG = 3
GB = 4
BR = 5

#iterations = 10000

overLap = np.zeros(6)

#for i in range(0,iterations):
#    for j in range(0,74):
#        trueSampleLoc[j,0] = j
#        f = 0
#        while f == 0:
#            x = np.random.randint(0,12)
#            if chromeLen[x] >= sampleLen[j]:
#                f = f+1
#        trueSampleLoc[j,1] = x
#        trueSampleLoc[j,2] = (chromeLen[x]-sampleLen[j])*np.random.rand()
#        trueSampleLoc[j,3] = trueSampleLoc[j,2]+sampleLen[j]
for j in range(0,74):
    for k in range(j+1,74):
        if trueSampleLoc[j,1] == trueSampleLoc[k,1]:
            if trueSampleLoc[k,2] <= trueSampleLoc[j,3]:
                if trueSampleLoc[k,3] >= trueSampleLoc[j,2]:
                    if trueSampleLoc[j,5] == RED:
                        if trueSampleLoc[k,5] == RED:
                            overLap[RR] = overLap[RR]+1
                        if trueSampleLoc[k,5] == GREEN:
                            overLap[RG] = overLap[RG]+1
                        if trueSampleLoc[k,5] == BLUE:
                            overLap[BR] = overLap[BR]+1   
                    if trueSampleLoc[j,5] == GREEN:
                        if trueSampleLoc[k,5] == RED:
                            overLap[RG] = overLap[RG]+1
                        if trueSampleLoc[k,5] == GREEN:
                            overLap[GG] = overLap[GG]+1
                        if trueSampleLoc[k,5] == BLUE:
                            overLap[GB] = overLap[GB]+1
                    if trueSampleLoc[j,5] == BLUE:
                        if trueSampleLoc[k,5] == RED:
                            overLap[BR] = overLap[BR]+1
                        if trueSampleLoc[k,5] == GREEN:
                            overLap[GB] = overLap[GB]+1
                        if trueSampleLoc[k,5] == BLUE:
                            overLap[BB] = overLap[BB]+1
np.savetxt("trueSampleOverlap.txt", overLap)