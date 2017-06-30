"""
Will parse blast output to identify a physical interval in the tomato genome to look for candidates.
"""

from __future__ import division
import argparse
import logging as log
import sys


def parse(file):
    log.debug("Parsing blast output " + file)
    blastOutput = open(file, "rU")
    topHits = {}
    for i, line in enumerate(blastOutput):
        cols = line.replace("\n", "").split()
        if line.startswith("#"):
            hitCount = 0
        else:
            if hitCount == 0:
                topHits[cols[0]] = [cols[1], cols[2], cols[8], cols[9]]
                hitCount += 1
    blastOutput.close()
    return topHits

def checkGroups(intervals, group, mask):
    toRemove = []
    markerMask = mask.split(",")
    for key, val in intervals.items():
        if val[0] != group:
            toRemove.append(key)
        elif key in markerMask:
            toRemove.append(key)
    for key in toRemove:
        log.debug("Removing key")
        del intervals[key]
    return intervals

def getInterval(intervals):
    allPositions = []
    for key, val in intervals.items():
        allPositions.append(int(val[2]))
        allPositions.append(int(val[3]))
    return min(allPositions), max(allPositions)

def compileHits(topHits):
    counts = {}
    for key, val in topHits.items():
        gene = val[0]
        if gene in counts.keys():
            counts[gene] += 1
        else:
            counts[gene] = 1
    log.debug(len(counts))
    return counts

def writeSummary(file, summary, topHits, lods):
    file1 = open(file, "w")
    file1.write("#Gene hits for ITAG3.2\n")
    file1.write("\n".join(summary.keys()))
    file1.write("\n")
    for key, val in topHits.items():
        file1.write(key + "\t" + val[0] + "\t" + lods[key][0] + "\t" + lods[key][1] + "\t" + val[1] + "\n")
    file1.close()

def getLODS(topHits, scanOut):
    f = open(scanOut, "rU")
    lodByMarker = {}
    for i, line in enumerate(f):
        if i == 0:
            continue
        else:
            l = line.replace("\n", "").split()
            lodByMarker[l[0]] = [l[3], l[2]]
    return lodByMarker

def main(*args):
    """Main function"""
    parser = argparse.ArgumentParser(description="Calculate Fst at each SNP location between populations")
    parser.add_argument("-v","--verbose", help="Enable debugging messages to be displayed", action='store_true')
    parser.add_argument("-p","--path", help="Path to input blast9 output file")
    parser.add_argument("-o","--output", help="Output path with file name")
    parser.add_argument("-g", "--group", help="Focal group string.")
    parser.add_argument("-m", "--mask", help="Marker mask.")
    parser.add_argument("-t", "--type", help="Type of database (cds or chromosomes).")
    parser.add_argument("-s", "--scanout", help="Scanone() raw output")


    args = parser.parse_args()
    if args.verbose:
        log.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d:%I:%M:%S%p',level=log.DEBUG)

    if args.type == "chromosomes":
        intervals = parse(args.path)
        intervals = checkGroups(intervals, args.group, args.mask)
        log.debug(intervals)
        left, right = getInterval(intervals)
        log.debug(left)
        log.debug(right)
        length = right-left
        log.debug(length)
    else:
        topHits = parse(args.path)
        for key, val in topHits.items():
            print key, val
            
        lods = getLODS(topHits, args.scanout)

        summary = compileHits(topHits)
        for key, val in summary.items():
            log.debug(key)
        writeSummary(args.output, summary, topHits, lods)

if __name__ == "__main__":
    main(*sys.argv)
