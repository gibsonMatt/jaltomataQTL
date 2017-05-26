#Will take a map file output from JoinMap and the genotypes from the joinmap input and generate a
#csv file that will input into r/qtl for actual QTL scanning. 

map1 = open("map_all.txt", 'rU')
genotypes = open("batch_1.genotypes_20.formatted.loc", "rU")
out1 = open("batch_1.genotypes_20.rqtl", "w")
structure = {}
individuals = []
#INPUT MAP
for i, line in enumerate(map1):
	if i == 0:
		continue
	else:
		l = line.replace("\n", "").split()
		lis = [int(l[2]), float(l[3])]
		structure[int(l[1])] = lis
map1.close()
#INPUT GENOTYPES
for i, line in enumerate(genotypes):
	if i in [0,1,2,3,4]:
		continue
	else:
		if line.startswith("indi"):
			continue
		if line.startswith("BC"):
			individuals.append(line)
		else:
			l = line.replace("\n", "").split()
			marker = int(l[0])
			gen = l[1:]
			
			if marker in structure:
				structure[marker].append(gen)
genotypes.close()
print len(structure)
print len(individuals)
structure = sorted(structure.items(), key=lambda x:(x[1][0],x[1][1]))
print "# INDIV" + str(len(individuals))

#right now I have a data structure sorted by group and position. Just need to print it out correctly......
#Marker names
for key in structure:
	out1.write(str(key[0])+",")
out1.write("\n")

#Linkage Groups
for key in structure:
	out1.write(str(key[1][0])+",")
out1.write("\n")

#Positions
for key in structure:
	out1.write(str(key[1][1])+",")
out1.write("\n")

count = 0
#Calls
for i in range(0, len(individuals)):
	out1.write(individuals[i].replace("\n", "") + ",")
	for val in structure:
		#print val[1][2][i]
		out1.write(str(val[1][2][i]) + ",")
	out1.write("\n")
out1.close()