"""
Takes input from a preliminary linkage map and will remove markers based on surrounding genotypes. 
If the left and right genotypes differ across many individuals, probably should remove that marker... 

"""

import argparse
import logging as log
import sys

import numpy as np
import pandas as pd
from pandas import DataFrame, Series


def readCross(file1):
    #file1 = open(sys.argv[1], "rU")
    markerOrder = []
    genotypesByMarker = {}
    markerGroups = {}
    markerPositions = {}
    for i, line in enumerate(file1):
        if i == 0:
            next
        elif i == 1:
            l = line.replace("\n", "").split(",")
            indvList = l[3:]
            log.debug("Individuals: " + str(len(indvList)))
        elif i > 1:
            l = line.replace("\n", "").split(",")
            name = l[0]
            markerGroups[name] = l[1]
            markerOrder.append(name)
            markerPositions[name] = float(l[2])
            genotypes = l[3:]
            genotypesByMarker[name] = genotypes
    file1.close()
    log.debug(str(len(genotypesByMarker)) + " markers total")
    return genotypesByMarker, indvList, markerOrder, markerGroups, markerPositions

def identifyMarkers(genotypesByMarker, markerOrder, penalty, threshold, markerGroups, groups):
    """Docstring"""
    markers2remove = []
    for i, marker in enumerate(markerOrder):
        score = 0.0
        if (i != 0) and (i != len(markerOrder)-1):
            leftMarkerName = markerOrder[i-1]
            rightMarkerName = markerOrder[i+1]
            centerMarkerName = marker
            if (markerGroups[leftMarkerName] != markerGroups[centerMarkerName]) or (markerGroups[rightMarkerName] != markerGroups[centerMarkerName]):
                #On diff groups...don't compare
                continue
            if groups != False:
                if markerGroups[centerMarkerName] not in groups:
                    continue
            leftGenotypes = genotypesByMarker[leftMarkerName]
            rightGenotypes = genotypesByMarker[rightMarkerName]
            centerGenotypes = genotypesByMarker[centerMarkerName]

            for indv, centerG in enumerate(centerGenotypes):
                leftG = leftGenotypes[indv]
                rightG = rightGenotypes[indv]
                if centerG != leftG:
                    score += penalty
                if centerG != rightG:
                    score += penalty
        if score >= threshold:
            markers2remove.append(centerMarkerName)
    log.debug("Removing " + str(len(markers2remove)) + " markers")
    return markers2remove

def fixCalls(genotypesByMarker, markerOrder, markerGroups, groups):
    """Docstring"""
    fixed = 0
    for i, marker in enumerate(markerOrder):
        if (i != 0) and (i != len(markerOrder)-1):
            leftMarkerName = markerOrder[i-1]
            rightMarkerName = markerOrder[i+1]
            centerMarkerName = marker
            if (markerGroups[leftMarkerName] != markerGroups[centerMarkerName]) or (markerGroups[rightMarkerName] != markerGroups[centerMarkerName]):
                #On diff groups...don't compare
                continue
            if groups != False:
                if markerGroups[centerMarkerName] not in groups:
                    continue
            leftGenotypes = genotypesByMarker[leftMarkerName]
            rightGenotypes = genotypesByMarker[rightMarkerName]
            centerGenotypes = genotypesByMarker[centerMarkerName]

            for indv, centerG in enumerate(centerGenotypes):
                leftG = leftGenotypes[indv]
                rightG = rightGenotypes[indv]
                if (centerG != rightG) and (centerG != leftG):
                    if rightG == leftG:
                        if rightG != '-':
                            fixed += 1
                            genotypesByMarker[marker][indv] = leftG
        elif (i == 0):
            rightMarkerName = markerOrder[i+1]
            centerMarkerName = marker
            if groups != False:
                if markerGroups[centerMarkerName] not in groups:
                    continue
            rightGenotypes = genotypesByMarker[rightMarkerName]
            centerGenotypes = genotypesByMarker[centerMarkerName]

            for indv, centerG in enumerate(centerGenotypes):
                print "i"
                rightG = rightGenotypes[indv]
                if (centerG != rightG):
                    if rightG != '-':
                        print "i"
                        fixed += 1
                        genotypesByMarker[marker][indv] = rightG

        elif (i == len(markerOrder)-1):
            print "r"
            leftMarkerName = markerOrder[i-1]
            centerMarkerName = marker
            if groups != False:
                if markerGroups[centerMarkerName] not in groups:
                    continue
            leftGenotypes = genotypesByMarker[leftMarkerName]
            centerGenotypes = genotypesByMarker[centerMarkerName]

            for indv, centerG in enumerate(centerGenotypes):
                leftG = leftGenotypes[indv]
                if (centerG != leftG):
                    print "r"
                    if leftG != '-':
                        fixed += 1
                        genotypesByMarker[marker][indv] = leftG

    log.debug("Fixed " + str(fixed) + " markers")
    return genotypesByMarker
#def missingFilter(genotyesByMarker, threshold)
    """Not implemented yet"""

def removeMarkers(genotypesByMarker, markerOrder, markerGroups, markerPositions, badMarkers):
    """Will remove the bad markers"""
    for marker in badMarkers:
        del genotypesByMarker[marker]
        del markerGroups[marker]
        del markerPositions[marker]
        markerOrder.remove(marker)
    return genotypesByMarker, markerOrder, markerGroups, markerPositions

def outputRQTL(name, genotypesByMarker, markerGroups, markerPositions):
    """Will output to an RQTL format file"""
    log.debug("Writing to RQTL format")
    for marker, genotypes in genotypesByMarker.items():
        genotypes.insert(0,markerPositions[marker])
        genotypes.insert(0, markerGroups[marker])

    frame = DataFrame.from_dict(genotypesByMarker, orient='index')
    frame = frame.sort_values(by=[0, 1],ascending=[1,1])
    frame = frame.transpose()
    frame = frame.replace(['AB','AA', 'BB'], ['H', 'A', 'B'])
    #sortedFrame = frame.sort_values(by=['0', '1'], ascending=[1,1], axis='columns')
    frame.to_csv(name, sep=",")


def main(*args):
    """Main function"""
    parser = argparse.ArgumentParser(description="Calculate Fst at each SNP location between populations")
    parser.add_argument("-v","--verbose", help="Enable debugging messages to be displayed", action='store_true')
    parser.add_argument("-i","--inputType", help="Type of input file (csvr)")
    parser.add_argument("-p","--path", help="Path to input file")
    parser.add_argument("-q","--penalty", help="Penalty to be applied")
    parser.add_argument("-t","--threshold", help="Penalty threshold to remove a marker")
    parser.add_argument("-m","--missing", help="Proportion missing threshold")
    parser.add_argument("-d","--dry", help="Run but don't output a file. Just shows diagnostics. Use with -v flag.", action='store_true')
    parser.add_argument('-f', "--fix", help="Fix calls instead of remove markers", action = 'store_true')
    parser.add_argument('-r', "--rounds", help="Fix calls instead of remove markers")
    parser.add_argument('-g', "--groups", help="Specify which LGs to analyze. Defaults to all.")
    args = parser.parse_args()
    if args.verbose:
        log.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d:%I:%M:%S%p',level=log.DEBUG)

    file = open(args.path, "rU")
    if len(args.groups) > 1:
        groups = args.groups
        groups = groups.split(",")
    else:
        groups = False
    genotypesByMarker, individuals, markerOrder, markerGroups, markerPositions = readCross(file)
    if args.fix != True:
        badMarkers = identifyMarkers(genotypesByMarker, markerOrder, float(args.penalty), float(args.threshold), markerGroups, groups)
        genotypesByMarker, markerOrder, markerGroups, markerPositions = removeMarkers(genotypesByMarker, markerOrder, markerGroups, markerPositions, badMarkers)
    else:
        for i in range(1, int(args.rounds)+1):
            log.debug("Round " + str(i) + " of fixing calls...")
            genotypesByMarker = fixCalls(genotypesByMarker, markerOrder, markerGroups, groups)
            badMarkers = identifyMarkers(genotypesByMarker, markerOrder, float(args.penalty), float(args.threshold), markerGroups, groups)
            genotypesByMarker, markerOrder, markerGroups, markerPositions = removeMarkers(genotypesByMarker, markerOrder, markerGroups, markerPositions, badMarkers)
        
    if args.dry != True:
        outputRQTL('data.rqtl.csv', genotypesByMarker, markerGroups, markerPositions)


if __name__ == "__main__":
    main(*sys.argv)
