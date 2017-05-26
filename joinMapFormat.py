
#!/usr/bin/env python
import sys



def replaceItems(genotypes, initial, new):
    newList = []
    for g in genotypes:
        if g == initial:
            newList.append(new)
        else:
            newList.append(g)
    return newList




#At what number column is the last phenotype
markerStart = int(sys.argv[1])


crossName = "Jsi6Jum2BC1"
crossType = "BC1"


input1 = open("Jsi6Jum2BC1_geno_repropheno3.csv", "rU")

#mapFile = open("map.map", "w")
genoFile = open("Jsi6Jum2BC1.loc", "w")
quantFile = open("quant.quant", "w")


#a = L
#b = P
genotypes = []

i = 0
for line in input1:
    l = line.replace("\n", "").split(",")

    #markers
    if i == 0:
        markers = l[markerStart:]
    #groups
    if i == 1:
        groups = l[markerStart:]
    #positions
    #if i == 2:
    #    positions = l[markerStart:]
    
    #genotypes
    if i > 1:
        print line
        l = replaceItems(l[markerStart:], "A", "a")
        l = replaceItems(l, "B", "b")
        l = replaceItems(l, "H", "h")
        l = replaceItems(l, "X", "-")
        genotypes.append(l)
    print i
    i += 1


#print genotypes


#Catch
#if (len(markers) != len(groups)):
#    print "ERROR IN LIST LENGTHS"
#    exit(0)
#if len(markers) != len(genotypes[0]):
#    print "ERROR! MARKER LIST LONGER THAN GENOTYPES"
#    exit(0)

###PRINTING OUT###

####MAP####
#prevGroup = "XX"
#for i, m in enumerate(markers):
#    if groups[i] != prevGroup:
#        mapFile.write("group" + "\t" + groups[i] + "\n")
#        prevGroup = groups[i]
#    mapFile.write(m + "\t" + positions[i] + "\n")
#
####GENOTYPES####
genoFile.write("name = " + crossName + "\n")
genoFile.write("popt = " + crossType + "\n")
genoFile.write("nloc = " + str(len(markers)) + "\n")
genoFile.write("nind = " + str(len(genotypes)) + "\n")
for x in range(0, len(markers)):
    Mstring = ""
    for i, m in enumerate(genotypes):
        Mstring = Mstring + m[x]
    genoFile.write(markers[x] + "\n")
    genoFile.write("\t" + Mstring + "\n")

####QUANTITATIVE DATA####


#mapFile.close()
genoFile.close()
input1.close()
