import numpy as np

##################################################################
# This is the file that checks the overlap of the random samples #
##################################################################

nSamples      = 74
nChromes      = 12

randSampleLoc = np.zeros([nSamples,4])
y1            = np.loadtxt('sampleLength.txt')
y2            = np.loadtxt('chromeLength.txt')
sampleLen     = y1[:,1]
sampleColor   = y1[:,2]
chromeLen     = y2[:,1]

RED   = 0
GREEN = 1
BLUE  = 2

RR = 0
GG = 1
BB = 2
RG = 3
GB = 4
BR = 5

iterations = 10000

overLap = np.zeros([iterations,6])

for i in range(0,iterations):
    for j in range(0,74):
        randSampleLoc[j,0] = j
        f = 0
        while f == 0:
            x = np.random.randint(0,12)
            if chromeLen[x] >= sampleLen[j]:
                f = f+1
        randSampleLoc[j,1] = x
        randSampleLoc[j,2] = (chromeLen[x]-sampleLen[j])*np.random.rand()
        randSampleLoc[j,3] = randSampleLoc[j,2]+sampleLen[j]
    for j in range(0,74):
        for k in range(j+1,74):
            if randSampleLoc[j,1] == randSampleLoc[k,1]:
                if randSampleLoc[k,2] <= randSampleLoc[j,3]:
                    if randSampleLoc[k,3] >= randSampleLoc[j,2]:
                        if sampleColor[j] == RED:
                            if sampleColor[k] == RED:
                                overLap[i,RR] = overLap[i,RR]+1
                            if sampleColor[k] == GREEN:
                                overLap[i,RG] = overLap[i,RG]+1
                            if sampleColor[k] == BLUE:
                                overLap[i,BR] = overLap[i,BR]+1   
                        if sampleColor[j] == GREEN:
                            if sampleColor[k] == RED:
                                overLap[i,RG] = overLap[i,RG]+1
                            if sampleColor[k] == GREEN:
                                overLap[i,GG] = overLap[i,GG]+1
                            if sampleColor[k] == BLUE:
                                overLap[i,GB] = overLap[i,GB]+1
                        if sampleColor[j] == BLUE:
                            if sampleColor[k] == RED:
                                overLap[i,BR] = overLap[i,BR]+1
                            if sampleColor[k] == GREEN:
                                overLap[i,GB] = overLap[i,GB]+1
                            if sampleColor[k] == BLUE:
                                overLap[i,BB] = overLap[i,BB]+1
np.savetxt("randomSampleOverlap.txt", overLap)