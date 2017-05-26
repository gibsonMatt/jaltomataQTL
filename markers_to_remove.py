inputF = open("out.filtered_5.hap", "rU")
markerOutput = open("markersToRemove.txt", "w")

markers = []

parentGenotypes = {}
offspring = {}
for i, line in enumerate(inputF):
    if i == 0:
        markers = line.replace("\n", "").split(",")
    else:
        gt = line.replace("\n", "").split(",")
        if gt[0] == "F1_4Filtered_1P.fq-aligned.sam.bam.sorted.bam":
            parentGenotypes["F1"] = gt[1:]
        elif gt[0] == "Jsi6Filtered_1P.fq-aligned.sam.bam.sorted.bam":
            parentGenotypes["Jsi"] = gt[1:]
        elif gt[0] == "Jum2Filtered_1P.fq-aligned.sam.bam.sorted.bam":
            parentGenotypes["Jum"] = gt[1:]
        else:
            name = gt[0].split(".")[0]
            if not name.startswith("F1"):
                offspring[name] = gt[1:]

def possibleF1(p1, p2):

	codes = {'R': ['A','G'], 'Y': ['C','T'], 'W': ['A','T'], 'S': ['G', 'C'], 'M': ['A','C'], 'K': ['G','T'],
		'A': ['A','A'], 'T': ['T','T'], 'G':['G','G'], 'C': ['C','C']}

	possibleF1 = []
	possibleF1.append(codes[p1][0] + codes[p2][0])
	possibleF1.append(codes[p1][1] + codes[p2][0])
	possibleF1.append(codes[p1][0] + codes[p2][1])
	possibleF1.append(codes[p1][1] + codes[p2][1])

	new = []

	for i, item in enumerate(possibleF1):
		if (item == 'AG') or (item == 'GA'):
			new.append('R')
		elif item == 'CT' or item == 'TC':
			new.append('Y')
		elif item == 'AT' or item == 'TA':
			new.append('W')
		elif item == 'GC' or item == 'CG':
			new.append('S')
		elif item == 'AC' or item == 'CA':
			new.append('M')
		elif item == 'GT' or item == 'TG':
			new.append('K')
		elif item == 'AA':
			new.append('A')
		elif item == 'TT':
			new.append('T')
		elif item == 'CC':
			new.append('C')
		elif item == 'GG':
			new.append('G')


	return new
	


markersToRemove = []
xsRemoved = []
for x in range(0, len(parentGenotypes["Jsi"])):
    if (parentGenotypes['Jsi'][x] == "N") and (parentGenotypes['Jum'][x] == "N"):
        markersToRemove.append(markers[x])
        xsRemoved.append(x)
    elif (parentGenotypes['Jsi'][x] != "N") and (parentGenotypes['Jum'][x] != "N"):
        try:
            possible = possibleF1(parentGenotypes['Jsi'][x], parentGenotypes['Jum'][x])
            if parentGenotypes["F1"][x] not in possible:
                marker = markers[x]
                if marker not in markersToRemove:
                    markersToRemove.append(marker)
                    xsRemoved.append(x)
        except KeyError:
            continue
        
for x in range(0, len(parentGenotypes['Jsi'])):
    freqMissing = 0.0
    countMissing = 0
    if x not in xsRemoved:
        for name, genotypes in offspring.items():
            if genotypes[x] == 'N':
                countMissing += 1
        freqMissing = float(float(countMissing)/len(offspring))
        if freqMissing > .3:
            marker = markers[x]
            if marker not in markersToRemove:
                markersToRemove.append(marker)
                xsRemoved.append(x)




for m in markersToRemove:
    markerOutput.write(m + "\n")

print "Number markers before filter: "
print len(markers)
print "Number of markers being removed: "
print len(markersToRemove)
print "Number of markers after removal: "
print (len(markers) - len(markersToRemove))

markerOutput.close()
inputF.close()