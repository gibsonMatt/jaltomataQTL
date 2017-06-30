"""
Will compiel separate files for each QTL containing consensus sequences.
"""

import argparse
import logging as log
import sys

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

def readQTL(file):
    f = open(file, "rU")
    markers_by_qtl = {}
    prevGroup = ""
    for line, marker in enumerate(f):
        if line == 0:
            continue
        else:
            l = marker.replace("\n", "").split(",")
            group = l[1].replace("\"", "")
            mark = l[0].replace("\"", "")
            if group != prevGroup:
                markers_by_qtl[group] = [mark]
                prevGroup = group
            else:
                markers_by_qtl[group].append(mark)
    f.close()
    return markers_by_qtl

def getSeq(file, markers):
    f = open(file, "rU")
    seqs_by_qtl = {}
    allMarkers = []
    allSeq = {}
    for group, markers1 in markers.items():
        for m in markers1:
            allMarkers.append(m)
    offset = 0
    get = False
    for line, seq in enumerate(f):
        seq = seq.replace("\n", "")
        if seq.startswith(">"):
            if seq.replace(">", "") in allMarkers:
                get = True
                marker = seq.replace(">", "")
        else:
            if get == True:
               allSeq[marker] = seq
               get = False
               marker = ""

    marks_by_group = {}
    for key, val in markers.items():
        markList = []
        group = key
        seqs_by_qtl[group] = []
        for mark in val:
            markList.append(mark)
            seqs_by_qtl[group].append(allSeq[mark])
        marks_by_group[group] = markList
    f.close()
    return seqs_by_qtl, marks_by_group

def main(*args):
    """Main function"""
    parser = argparse.ArgumentParser(description="Calculate Fst at each SNP location between populations")
    parser.add_argument("-v","--verbose", help="Enable debugging messages to be displayed", action='store_true')
    parser.add_argument("-p","--path", help="Path to input consensus sequence fasta file")
    parser.add_argument("-q","--qtl", help="Path to input qtl marker file")
    parser.add_argument("-o","--output", help="Output path.")


    args = parser.parse_args()
    if args.verbose:
        log.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d:%I:%M:%S%p',level=log.DEBUG)

    qtlMarkers = readQTL(args.qtl)
    #print qtlMarkers
    #print len(qtlMarkers["L.3"])

    seqs, markList = getSeq(args.path, qtlMarkers)
    for key, val in seqs.items():
        outname = key + ".consensus.fa" 
        out = open(outname, "w")
        for i, m in enumerate(val):
            markerName = markList[key][i]
            out.write(">" + markerName + "\n" + m + "\n")

if __name__ == "__main__":
    main(*sys.argv)
