file1 = open("markersToRemove.txt", "rU")

out1 = open("newMarkersToRemove.txt", "w")

#SSL3.0ch04_25365830
for line in file1:
   # l = line.split("_")
    newLine = line[0:5]+"CH"+line[7:]
    #print newLine
    out1.write("S" + newLine.replace("\n", "") + " ")

file1.close()
out1.close()