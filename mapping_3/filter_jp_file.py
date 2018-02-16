"""
Will take in the Joinmap output from Stacks, filter markers based on #s of individual calls,
and output a new file--either in R/QTL format, Joinmap, or Linkage.

#FOR BACKCROSS 1 POPULATIONS ONLY
"""
import sys
import argparse
import logging as log


def importJPFile(file):
    """Will input data from joinmap file"""
    genotypeDic = {}
    nameTrig = False
    indvNames = []
    for i, line in enumerate(file):
        cols = line.replace("\n", "").split()
        if i == 0:
            name = cols[2]
        elif i == 1:
            pop = cols[2]
        elif i == 2:
            nloc = cols[2]
        elif i == 3:
            nind = cols[2]
        elif len(cols) == 0:
            continue
        elif line.startswith("individual names:"):
            nameTrig = True
        elif nameTrig == True:
            indvNames.append(cols[0])
        elif i > 4:
            genotypeDic[cols[0]] = cols[2:]
    file.close()
    return name, pop, nind, nloc, genotypeDic, indvNames

def filterByMarker(genotypes, threshold):
    """Filters based on #s of individuals called per marker
    Will also remove any capital letter calls (not yet)
    """
    newDict = {}
    markersToRemove = []
    log.debug("Filtering markers. Minimum # of individuals calls = " + str(threshold))
    for key, val in genotypes.items():
        missing = 0
        for i, call in enumerate(val):
            if call in ['-', 'NA', 'X']:
                missing += 1
        if (len(val) - missing) <= threshold:
            markersToRemove.append(key)
    log.debug("Removing " + str(len(markersToRemove)) + " markers")

    for marker in markersToRemove:
        del genotypes[marker]

    for key, val in genotypes.items():
        newList = []
        for i, call in enumerate(val):
            if call in ['b', '-', 'h']:
                newList.append(call)
            elif call == 'B':
                newList.append('b')
            elif (call == 'A') or (call == 'a'):
                newList.append('-')
            elif call == 'H':
                newList.append('h')
        newDict[key] = newList
    return newDict, len(markersToRemove)


def rqtlOutput(genotypes, file, nloc, nind, individuals):
    """Will output to R/QTL format"""
    genotypesByIndv = {}
    #Populate new dict with indv names
    for ind in individuals:
        genotypesByIndv[ind] = []
    markerOrder = []
    for i in range(0, int(nind)):
        for marker, calls in genotypes.items():
            if i == 0:
                markerOrder.append(marker)
            genotypesByIndv[individuals[i]].append(calls[i])

    #Actually write out the file
    ones =["1"]*len(markerOrder)
    file.write("index,genotype," + ",".join(markerOrder) + "\n")
    file.write(",," + ",".join(ones) + "\n")
    index = 1
    for indv, calls in genotypesByIndv.items():
        file.write(str(index) + "," + indv + "," + ",".join(calls) + "\n")
        index += 1
    file.close()


def joinmapOutput(genotypes, file, name, pop, nloc, nind, individuals):
    file.write("name = " + name + "\n" + "popt = " + pop + "\n" + "nloc = " + str(nloc) + "\n" +
    "nind = " + str(nind) + "\n")

    for marker, calls in genotypes.items():
        file.write(marker + "\t" + "\t".join(calls) + "\n")

    file.write("individual names: \n")
    for ind in individuals:
        file.write(ind + "\n")
    file.close()

def linkageOutput(genotypes, file, fam, nind, individuals):
    """IS NOT CORRECT FORMAT"""
    genotypesByIndv = {}
    #Populate new dict with indv names
    for ind in individuals:
        genotypesByIndv[ind] = []
    markerOrder = []
    for i in range(0, int(nind)):
        for marker, calls in genotypes.items():
            if i == 0:
                markerOrder.append(marker)
            genotypesByIndv[individuals[i]].append(calls[i])
    newDic = {}
    for indv, calls in genotypesByIndv.items():
        newCalls = []
        for call in calls:
            if call == 'h':
                newCalls.append("1 2")
            elif call == 'b':
                newCalls.append("2 2")
            elif call == 'a':
                newCalls.append("1 1")
            elif call == '-':
                newCalls.append("0 0")
        newDic[indv] = newCalls
    if len(newDic) != len(genotypesByIndv):
        log.debug("ERROR")

    Bs = ['2 2']*len(markerOrder)
    As = ['1 1']*len(markerOrder)

    log.debug(len(Bs))
    i = 1
    file.write(fam + "\t" + "500"  + "\t" + "0" + "\t" + "0" + "\t" + "1" + "\t" + "0" + "\t"  + "\t".join(Bs) + "\n")
    file.write(fam + "\t" + "501" + "\t" + "0" + "\t" + "0" + "\t" + "2" + "\t" + "0" + "\t"   + "\t".join(As) + "\n")
    for indv, calls in newDic.items():
        file.write(fam + "\t" + str(i) + "\t" + "500" + "\t" + "501" +
                   "\t" + "0" + "\t" + "0" + "\t" + "\t".join(calls) + "\n")
        i += 1
   


    file.close()

def main(*args):
    """Main function"""
    parser = argparse.ArgumentParser(description="Convert between R/QTL and joinmap formats, with optional filtering")
    parser.add_argument("-v","--verbose", help="Enable debugging messages to be displayed", action='store_true')
    parser.add_argument("-i","--inputType", help="Type of input file (rqtl or joinmap)")
    parser.add_argument("-ot", "--outputType", help="Type of file to output to (rqtl, joinmap, or linkage)")
    parser.add_argument("-f", "--file", help="Path to input file")
    parser.add_argument("-t", "--threshold", help="Minimum # of individuals called to keep marker")
    parser.add_argument("-o", "--outname", help="Name for output file (with extension)")

    args = parser.parse_args()
    if args.verbose:
        log.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d:%I:%M:%S%p',level=log.DEBUG)

    if args.inputType == "joinmap":
        jpFile = open(args.file, "rU")
        name, pop, nind, nloc, genotypeDic, indvNames = importJPFile(jpFile)
        #log.debug("Motifs is %s\n Length: %d" % (motifs, len(motifs)))
        newDict, numRemoved = filterByMarker(genotypeDic, int(args.threshold))
        log.debug("File number of markers = " + str(len(newDict)))


        if args.outputType == "joinmap":
            log.debug("Exporting to joinmap format...")
            out1 = open(args.outname, "w")
            joinmapOutput(newDict, out1, name, pop, len(newDict), nind, indvNames)
        elif args.outputType == "rqtl":
            log.debug("Exporting to rqtl format...")
            out2 = open(args.outname, "w")
            rqtlOutput(newDict, out2, nloc, nind, indvNames)
        elif args.outputType == "linkage":
            log.debug("Exporting to linkage format...")
            out2 = open(args.outname, "w")
            linkageOutput(newDict, out2, "jalBC1", nind, indvNames)


if __name__ == "__main__":
    main(*sys.argv)
