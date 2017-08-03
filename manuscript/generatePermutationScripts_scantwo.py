#Will automate the generation of permutation test scripts for jaltomata QTL scanning.
#To be run on cluster

"""
Future:
    -Add arguments for specifying details
"""

import sys

def genScript(name, col, covar):
    fileName = name + "_p.R"
    file = open('./scantwo_scripts/' + fileName, "w")

    file.write("#" + name + "\n")
    file.write('library(qtl)\n')
    file.write('setwd("/N/dc2/projects/gibsonTomato/jaltomata/manuscript")\n')
    file.write('mapJal5.1 <- read.cross("csv","/N/dc2/projects/gibsonTomato/jaltomata/manuscript/data", "final_map_6_15_t.csv", genotypes=c("A", "H"), alleles=c("A", "B"), na.strings=c("-", "NA"), estimate.map=F,crosstype = "bc")\n')
    file.write('mapJal5.1 <- calc.genoprob(mapJal5.1, step=2)\nbench <- pull.pheno(mapJal5.1, pheno.col = 3)\nhmorph <- pull.pheno(mapJal5.1, pheno.col=c(3, 4))\nfmorph <- pull.pheno(mapJal5.1, pheno.col=c(3, 5))\
                \nhcolor <- pull.pheno(mapJal5.1, pheno.col=c(3, 6))\nfcolor <- pull.pheno(mapJal5.1, pheno.col=c(3, 7))\ncrossed <- pull.pheno(mapJal5.1, pheno.col=c(3, 8))\ntrichome <- pull.pheno(mapJal5.1, pheno.col=c(3,8))\
                \nveg <- pull.pheno(mapJal5.1, pheno.col=c(3, 10))\n')

    file.write(name + ' <- scantwo(mapJal5.1, pheno.col=' + col + ', method="em", addcovar=' + covar + ')\n')
    file.write(name + "\n")
    file.write('summary(' + name + ')\n')
    permName = name + '_p'
    file.write(permName + ' <- scantwo(mapJal5.1, pheno.col=' + col + ', method="em", addcovar=' + covar + ', n.perm=1000)\n')
    file.write('x <- summary(' + permName + ')\n')
    file.write('print(x)\n')
    file.write('summary(' + name + ', perms=' + permName + ', alpha=0.05, pvalues=T)\n')
    file.write('save(x, file="' + permName + '")\n')

    file.write('print(pen <- calc.penalties(' + permName + '))\n')
    stpWiseName = name + '_stpw'
    file.write(stpWiseName + '<- stepwiseqtl(mapJal5.1, max.qtl=5, penalties=pen, method="em", verbose=2)\n')
    file.write(stpWiseName + '\n')
    file.write('save(' + stpWiseName + ', file="' + stpWiseName + '")\n')
    file.close()


def main(*args):
    names = open(sys.argv[1], "rU")
    names_list = {}
    for i, line in enumerate(names):
        #scanName column covar
        l = line.replace("\n","").split(" ")
        names_list[l[0]] = [l[1], l[2]]
    names.close()
    for key, val in names_list.items():
        genScript(key, val[0], val[1])


if __name__ == "__main__":
    main(*sys.argv)
