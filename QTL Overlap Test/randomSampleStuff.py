import numpy as np

nSamples      = 74
nChromes      = 12

#################################################################
# This is the file that creates the randomized sample locations #
#################################################################

randSampleLoc = np.zeros([nSamples,4])          #initialize matrix
y1            = np.loadtxt('sampleLength.txt')  #load parameters for sample length
y2            = np.loadtxt('chromeLength.txt')  #load parameters for chrom length
sampleLen     = y1[:,1]
chromeLen     = y2[:,1]

for i in range(0,74):
    randSampleLoc[i,0] = i
    f = 0
    while f == 0:
        x                  = np.random.randint(0,12)
        if chromeLen[x] >= sampleLen[i]:
            f = f+1
    randSampleLoc[i,1] = x
    randSampleLoc[i,2] = (chromeLen[x]-sampleLen[i])*np.random.rand()
    randSampleLoc[i,3] = randSampleLoc[i,2]+sampleLen[i]
    
np.savetxt("randomSampleLocations.txt", randSampleLoc)