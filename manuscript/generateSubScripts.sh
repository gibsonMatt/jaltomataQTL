#!/bin/bash
#Will generate all qsub scripts for the permutation tests

#cd /N/dc2/projects/gibsonTomato/jaltomata/manuscript/data/scripts

for file in *.R
do
	echo "#PBS -k oe" > $file.sh
	echo "#PBS -l nodes=1:ppn=1,vmem=30gb,walltime=48:00:00" >> $file.sh
	echo "#PBS -M gibsomat@iu.edu" >> $file.sh
	echo "#PBS -m ae" >> $file.sh
	echo "#PBS -N $file-permutations" >> $file.sh
	echo "module load intel" >> $file.sh
	echo "module load curl" >> $file.sh
	echo "module load java" >> $file.sh
	echo "module load R" >> $file.sh
	echo "cd /N/dc2/projects/gibsonTomato/jaltomata/manuscript/data/scantwo_scripts" >> $file.sh	
	echo "Rscript $file > $file.out.txt" >> $file.sh
done

