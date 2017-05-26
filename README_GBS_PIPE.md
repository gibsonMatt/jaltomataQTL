# Jaltomata QTL mapping
New pipeline starting with multiplexed data
## Demultiplexing

###### Demultiplex files using STACKS `process_radtags`

```
#JC added haeIII, so I am calling Stacks manually. 

cd /N/dc2/projects/gibsonTomato/jaltomata/multiplexed/RawData

module load gcc/4.9.2

/N/dc2/projects/gibsonTomato/stacks-1.46/process_radtags -1 GBS00346_L2_1.fq.gz -2 GBS00346_L2_2.fq.gz -o ../output_346/ -b ../bar
codes/lib_346.txt --renz_1 mseI --inline_inline --renz_2 haeIII  -r -q -c -i gzfastq

```

###### Concatenate all four files for each individual

```
#For all of the in a library output directory
for rem1 in *.rem.1.fq.gz
do
        #Generate the other file names
        rem2=${rem1%%.1.fq.gz}".2.fq.gz"
        p1=${rem1%%.rem.1.fq.gz}".1.fq.gz"
        p2=${rem1%%.rem.1.fq.gz}".2.fq.gz"
        #Concatenate    
        cat $rem1 $rem2 $p1 $p2 > /N/dc2/projects/gibsonTomato/jaltomata/multiplexed/cat_output_335/${rem1%%.rem.1.fq.gz}".fq.gz"
done
```

###### Unzip
```
module load tabix
for p1 in *.fq.gz
do
        p2=${p1%%.gz}
        gzip -d -c $p1 > ../cat_output_unzip/$p2

done
```

## Stacks pipeline

Can get more data using denovo_map pipeline than using reference. Reference will act as a strict filter,
especially when it is far diverged.

###### `denovo_map.pl`
```
Going to use defaults first. See how many loci we get. 

cd /N/dc2/projects/gibsonTomato/jaltomata/multiplexed/cat_output_unzip/

/N/dc2/projects/gibsonTomato/stacks-1.46/scripts/denovo_map.pl -m 3 -M 3 -n 2 -T 15 -S -b 2 -A 'BC1' -X "genotypes:-o 'joinmap'" \
        -e /N/dc2/projects/gibsonTomato/stacks-1.46/ \
        -o /N/dc2/projects/gibsonTomato/jaltomata/multiplexed/stacks_denovo_output \
        -p Jsi6.fq \
        -p Jum2.fq \
        -r ...all individuals...
```

###### `genotypes`
So I ran the default pipeline, got the data into Joinmap, got LGs, but one was very small.
Marker ordering is taking forever with most methods, but using ASMap is fast. The only downside \
is that using ASMap results is very very large LGs, likely due to genotyping errors. 
I am going to re-run the `genotypes` program with the correction flag set. Hopefully this will give \
me a better set of markers...
Beyond this, I can explore using LinkImpute which will impute genotypes without knowledge of physical \
position. This may be hard to do as it requires a weird file format...not sure.
Alternatively, I could map consensus sequences against tomato, get physical order, then impute using \
typical methods...but hopefully `genotypes` will give good results. 

```
module load gcc/4.9.2

cd /N/dc2/projects/gibsonTomato/jaltomata/multiplexed/

/N/dc2/projects/gibsonTomato/stacks-1.46/genotypes -b 2 -r 3 -c -P /N/dc2/projects/gibsonTomato/jaltomata/multiplexed/stacks_denov
o_output -t 'BC1' -o 'joinmap'
```