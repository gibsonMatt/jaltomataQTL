#Removed all markers where P1 and P2 shared same genotype
#Removed every marker where F1 was a homozygote
#Removed everything where F1 was the wrong het
#



import sys
import copy
file1 = open("jaltomata_genotypes_names.csv", "rU")
out1 = open("MarkerData_new.csv", "w")

loci = []
genos = {}

for i, line in enumerate(file1):
	l = line.split(",")
	if i == 0:
		loci = l
	else:
		indvName = l[0]
		genotypes = l[1:]
		genos[indvName] = genotypes


#f1 = genos['F1-4']
f1 = genos['F1_4']
p1 = genos['Jsi6']
p2 = genos['Jum2']

markersToRemove = []


newf1 = ['']*len(f1)
newp1 = ['']*len(p1)
newp2 = ['']*len(p2)

geno_length = len(f1)

countNum_N = 0




del loci[0]
print loci[0]
#Think about assigning parents based on ALL F1 genotypes...
for x in range(0, geno_length):

	if p1[x] == p2[x]:
		newp1[x] = 'X'
		newp2[x] = 'X'
		newf1[x] = 'X'
		if x not in markersToRemove:
			markersToRemove.append(x)
		continue
	#Probably don't need since checking for possible F1s later...
	#if f1[x] in ['A', 'T', 'C', 'G']:
	#	if x not in markersToRemove:
	#		markersToRemove.append(x)
	#		continue

	if p1[x] in ['A', 'T', 'C', 'G'] and p2[x] in ['R', 'Y', 'W', 'S', 'M', 'K']:
		if f1[x] != p2[x]:
			newp1[x] = 'X'
			newp2[x] = 'X'
			newf1[x] = 'X'
			if x not in markersToRemove:
				markersToRemove.append(x)
			continue
	elif p1[x] in ['R', 'Y', 'W', 'S', 'M', 'K'] and p2[x] in ['R', 'Y', 'W', 'S', 'M', 'K']:
		if f1[x] != p2[x]:
			newp1[x] = 'X'
			newp2[x] = 'X'
			newf1[x] = 'X'
			if x not in markersToRemove:
				markersToRemove.append(x)
			continue


	if p1[x] == 'N':
		countNum_N += 1
#	if p1[x] == 'N':
#		if f1[x] == 'R':
#			if p2[x] == 'G':
#				newp1[x] = 'A'
#			elif p2[x] == 'A':
#				newp1[x] = 'G'
#			elif p2[x] == 'R':
#				newp1[x] = 'A'
#		elif f1[x] == 'Y':
#			if p2[x] == 'C':
#				newp1[x] = 'T'
#			elif p2[x] == 'T':
#				newp1[x] = 'C'
#			elif p2[x] == 'Y':
#				newp1[x] = 'C'
#		elif f1[x] == 'W':
#			if p2[x] == 'A':
#				newp1[x] = 'T'
#			elif p2[x] == 'T':
#				newp1[x] = 'A'
#			elif p2[x] == 'W':
#				newp1[x] = 'A'
#		elif f1[x] == 'S':
#			if p2[x] == 'G':
#				newp1[x] = 'C'
#			elif p2[x] == 'C':
#				newp1[x] = 'G'
#			elif p2[x] == 'S':
#				newp1[x] = 'G'
#		elif f1[x] == 'M':
#			if p2[x] == 'C':
#				newp1[x] = 'A'
#			elif p2[x] == 'A':
#				newp1[x] = 'C'
#			elif p2[x] == 'M':
#				newp1[x] = 'C'
#		elif f1[x] == 'K':
#			if p2[x] == 'G':
#				newp1[x] = 'T'
#			elif p2[x] == 'T':
#				newp1[x] = 'G'
#			elif p2[x] == 'K':
#				newp1[x] = 'G'
#		#Some of these could be hets too....
	if p2[x] == 'N':
		if f1[x] == 'R':
			if p1[x] == 'G':
				newp2[x] = 'A'
				next
			elif p1[x] == 'A':
				newp2[x] = 'G'
				next
			elif p1[x] == 'R':
				newp2[x] = 'G'
				next
		elif f1[x] == 'Y':
			if p1[x] == 'C':
				newp2[x] = 'T'
				next
			elif p1[x] == 'T':
				newp2[x] = 'C'
				next
			elif p1[x] == 'Y':
				newp2[x] = 'T'
				next
		elif f1[x] == 'W':
			if p1[x] == 'A':
				newp2[x] = 'T'
				next
			elif p1[x] == 'T':
				newp2[x] = 'A'
				next
			elif p1[x] == 'W':
				newp2[x] = 'T'
				next
		elif f1[x] == 'S':
			if p1[x] == 'G':
				newp2[x] = 'C'
				next
			elif p1[x] == 'C':
				newp2[x] = 'G'
				next
			elif p1[x] == 'S':
				newp2[x] = 'C'
				next
		elif f1[x] == 'M':
			if p1[x] == 'C':
				newp2[x] = 'A'
				next
			elif p1[x] == 'A':
				newp2[x] = 'C'
				next
			elif p1[x] == 'M':
				newp2[x] = 'A'
				next
		elif f1[x] == 'K':
			if p1[x] == 'G':
				newp2[x] = 'T'
				next
			elif p1[x] == 'T':
				newp2[x] = 'G'
				next
			elif p1[x] == 'K':
				newp2[x] = 'T'
				next
	

		if p1[x] == 'K' and f1[x] == 'R':
			newp2[x] = 'A'
		elif p1[x] == 'K' and f1[x] == 'S':
			newp2[x] = 'C'
		elif p1[x] == 'K' and f1[x] == 'W':
			newp2[x] = 'A'
		elif p1[x] == 'K' and f1[x] == 'Y':
			newp2[x] = 'G'
				
		elif p1[x] == 'M' and f1[x] == 'R':
			newp2[x] = 'G'
		elif p1[x] == 'M' and f1[x] == 'S':
			newp2[x] = 'G'
		elif p1[x] == 'M' and f1[x] == 'W':
			newp2[x] = 'T'
		elif p1[x] == 'M' and f1[x] == 'Y':
			newp2[x] = 'T'
				
		elif p1[x] == 'S' and f1[x] == 'R':
			newp2[x] = 'A'
		elif p1[x] == 'S' and f1[x] == 'M':
			newp2[x] = 'A'
		elif p1[x] == 'S' and f1[x] == 'K':
			newp2[x] = 'T'
		elif p1[x] == 'S' and f1[x] == 'Y':
			newp2[x] = 'T'
				
		elif p1[x] == 'W' and f1[x] == 'R':
			newp2[x] = 'G'
		elif p1[x] == 'W' and f1[x] == 'M':
			newp2[x] = 'C'
		elif p1[x] == 'W' and f1[x] == 'K':
			newp2[x] = 'G'
		elif p1[x] == 'W' and f1[x] == 'Y':
			newp2[x] = 'C'
					
		elif p1[x] == 'Y' and f1[x] == 'W':
			newp2[x] = 'A'
		elif p1[x] == 'Y' and f1[x] == 'M':
			newp2[x] = 'A'
		elif p1[x] == 'Y' and f1[x] == 'K':
			newp2[x] = 'G'
		elif p1[x] == 'Y' and f1[x] == 'S':
			newp2[x] = 'G'
					
		elif p1[x] == 'R' and f1[x] == 'W':
			newp2[x] = 'T'
		elif p1[x] == 'R' and f1[x] == 'M':
			newp2[x] = 'C'
		elif p1[x] == 'R' and f1[x] == 'K':
			newp2[x] = 'T'
		elif p1[x] == 'R' and f1[x] == 'S':
			newp2[x] = 'C'

	#If none of the parents were Ns and we didn't change anything, just assign it to what it was originally.
	if (newp1[x] == ''):
		newp1[x] = p1[x]
		next
	if (newp2[x] == ''):
		newp2[x] = p2[x]
		next

######
######
######
######!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#newp2[-1] = 'G'
#Are there any cases where parents are both homos and F1 isnt a het?? Or have those been removed?



print "Number of markers where P1 isn't 'N'"
print geno_length - countNum_N


out2 = open("MarkerData_intermediate.csv", "w")
out2.write("," + ",".join(loci))
for key, val in sorted(genos.items()):
	if key == 'Jum2':
		out2.write(key + "," + ",".join(val) + "\n")
	elif key == "F1_4":
		out2.write("\n" + key + "," + ",".join(val))
	else:
		out2.write(key + "," + ",".join(val))

out2.write("newp2" + "," + ",".join(newp2))
	
out2.close()
			

##########################################################################
#Backcross assignments
##########################################################################

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
	

	

def possibleKids(p1, p2, f1):
	codes = {'R': ['A','G'], 'Y': ['C','T'], 'W': ['A','T'], 'S': ['G', 'C'], 'M': ['A','C'], 'K': ['G','T'],
		'A': ['A','A'], 'T': ['T','T'], 'G':['G','G'], 'C': ['C','C']}
	possibleKids_i = {}
	possibleF1_i = possibleF1(p1,p2)

	reassigned = False
	if f1 == 'N':
		if (p1 in ['A', 'C', 'T', 'G']) and (p2 in ['A', 'C', 'T', 'G']):
			pf1 = [p1,p2]
			reassigned = True
			if (pf1 == ['A','G']) or (pf1 == ['G','A']):
				f1 = 'R'
			elif (pf1 == ['C','T']) or (pf1 == ['T','C']):
				f1 = 'Y'
			elif (pf1 == ['A','T']) or (pf1 == ['T','A']):
				f1 = 'W'
			elif (pf1 == ['G','C']) or (pf1 == ['C','G']):
				f1 = 'S'
			elif (pf1 == ['A','C']) or (pf1 == ['C','A']):
				f1 = 'M'
			elif (pf1 == ['G','T']) or (pf1 == ['T','G']):
				f1 = 'K'

	if (f1 not in possibleF1_i) or (f1 in ['A', 'C', 'T', 'G']):
		if not reassigned:
			return 'IMP'

	possibleKids_i = []
	possibleKids_i.append(codes[p1][0] + codes[f1][0])
	possibleKids_i.append(codes[p1][1] + codes[f1][0])
	possibleKids_i.append(codes[p1][0] + codes[f1][1])
	possibleKids_i.append(codes[p1][1] + codes[f1][1])

	new = []

	for i, item in enumerate(possibleKids_i):
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




#New dict to reassign BC genotypes in. Should this be a deep copy?
newGenos = copy.deepcopy(genos)

homozygotes = ['A', 'T', 'G', 'C']

#markersToRemove = []


#Now do all the BC individuals
for key, val in newGenos.items():
	#Making sure we dont compare parents to parents...or whatever
	#if key not in ['F1-4', 'Jsi6', 'Jum2']:
	if key not in ['F1_4', 'Jsi6', 'Jum2']:
		#looping through markers of an individual
		for x in range(0, geno_length):
			if newp1[x] == 'X':
				continue
			p1Call = newp1[x].replace('\n','')
			p2Call = newp2[x].replace('\n','')
			#f1Call = genos['F1-4'][x].replace('\n','')
			f1Call = genos['F1_4'][x].replace('\n','')
			bc = val[x].replace('\n','')
			newCall = ""
			if p1Call == 'N' or p2Call == 'N':
				newGenos[key][x] = 'X'
				if x not in markersToRemove:
					markersToRemove.append(x)
				next
			else:
				possibleKids_i = possibleKids(p1Call, p2Call, f1Call)

				if possibleKids_i == 'IMP':
					newGenos[key][x] = 'X'
					if x not in markersToRemove:
						markersToRemove.append(x)
					next
				else:
					if bc not in possibleKids_i:
						#print "BAD BC Call"
						newGenos[key][x] = 'X'
						newCall = 'X'
					else:
						#print p1Call, p2Call, f1Call, bc
						if (p1Call in ['R', 'Y', 'W', 'S', 'M', 'K']) and (p2Call in ['A', 'T', 'C', 'G']):
							if bc == p1Call:
								newGenos[key][x] = 'A'
								newCall = 'A'
							elif p1Call == 'R':
								if (bc == 'A') or (bc == 'G'):
									newGenos[key][x] = 'A'
									newCall = 'A'
								else:
									newCall = 'H'
									newGenos[key][x] = 'H'
							elif p1Call == 'Y':
								if (bc == 'C') or (bc == 'T'):
									newGenos[key][x] = 'A'
									newCall = 'A'
								else:
									newCall = 'H'
									newGenos[key][x] = 'H'
							elif p1Call == 'W':
								if (bc == 'A') or (bc == 'T'):
									newGenos[key][x] = 'A'
									newCall = 'A'
								else:
									newCall = 'H'
									newGenos[key][x] = 'H'
							elif p1Call == 'S':
								if (bc == 'G') or (bc == 'C'):
									newGenos[key][x] = 'A'
									newCall = 'A'
								else:
									newCall = 'H'
									newGenos[key][x] = 'H'
							elif p1Call == 'M':
								if (bc == 'A') or (bc == 'C'):
									newGenos[key][x] = 'A'
									newCall = 'A'
								else:
									newCall = 'H'
									newGenos[key][x] = 'H'
							elif p1Call == 'K':
								if (bc == 'G') or (bc == 'T'):
									newGenos[key][x] = 'A'
									newCall = 'A'
								else:
									newCall = 'H'
									newGenos[key][x] = 'H'
							#else:
						#		newCall = 'H'
						#		newGenos[key][x] = 'H'
							
						elif (p1Call in ['A', 'T', 'C', 'G']) and (p2Call in ['R', 'Y', 'W', 'S', 'M', 'K']):
							#print "I RAN"
							if bc == p1Call:
								newGenos[key][x] = 'A'
							elif bc in ['R', 'Y', 'W', 'S', 'M', 'K']:
								newGenos[key][x] = 'H'
						
						elif (p1Call in ['A', 'T', 'C', 'G'] and p2Call in ['A', 'T', 'C', 'G']):
							if bc == p1Call:
								newGenos[key][x] = 'A'
							elif bc in ['R', 'Y', 'W', 'S', 'M', 'K']:
								newGenos[key][x] = 'H'
						elif p1Call in ['R', 'Y', 'W', 'S', 'M', 'K'] and p2Call in ['R', 'Y', 'W', 'S', 'M', 'K']:
							if bc == p1Call:
								newGenos[key][x] = 'A'
							elif bc in ['A', 'T', 'C', 'G']:
								newGenos[key][x] = 'A'
							elif bc in ['R', 'Y', 'W', 'S', 'M', 'K']:
								newGenos[key][x] = 'H'
							
						#elif bc == p1Call:
						#	newGenos[key][x] = 'A'
						#	newCall = 'A'
						#elif bc == p2Call:
						#	newGenos[key][x] = 'X*'
						#	newCall = 'X'
							#print "HOMOZYGOUS FOR P2"
						#else:
						#	newCall = 'H'
						#	newGenos[key][x] = 'H'
				#print p1Call, p2Call, f1Call, bc, possibleKids_i,  newGenos[key][x]

				if newGenos[key][x] in ['C', 'T', 'G', 'R', 'Y', 'W', 'S', 'M', 'K']:
					print "ASSIGNED NO CALL TO BC INDIVIDUAL"
					exit(0)

print "Removing " + str(len(markersToRemove)) + " markers"
#Should write a txt file with the removed markers here....
for key, val in newGenos.items():
	#Making sure we dont compare parents to parents...or whatever
	#if key not in ['F1-4', 'Jsi6', 'Jum2']:
		#looping through markers of an individual
		#indexes = [2, 3, 5]
	for index in sorted(markersToRemove, reverse=True):
		del val[index]
#Remove from marker list
for index in sorted(markersToRemove, reverse=True):
		del loci[index]
		del newp2[index]
print len(loci)
print len(newGenos['BC1_100'])
#Write new table/////////////

lgs = ['1']*len(loci)

out1.write("," + ",".join(loci) + '\n')
out1.write("," + ",".join(lgs) + '\n')
out1.write('\n')
for key, val in sorted(newGenos.items()):
	out1.write(key + "," + ",".join(val) + "\n")
out1.write("newP2" + "," + ",".join(newp2) + "\n")

#out2.write("newp2" + "," + ",".join(newp2))
	




			


out1.close()
file1.close()