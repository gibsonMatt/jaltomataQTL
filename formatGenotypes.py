file1 = open("batch_1.genotypes_50.rqtl.tsv", "rU")

out1 = open("batch_1.genotypes_50.rqtl.formatted.tsv", "w")

for i, line in enumerate(file1):
	if i == 0:
		l = line.split(",")
		print len(l)
		out1.write(line)
		continue
	elif i == 1:
		l = line.split(",")
		print len(l)
		out1.write(line)
		continue
	elif i == 2:
		l = line.split(",")
		print len(l)
		out1.write(line)
		continue
	l = line.split(",")
	l2 = l[0:5493]
	print len(l)
	out1.write("," + ",".join(l2)+"\n")
file1.close()
out1.close()
