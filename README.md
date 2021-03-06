# Jaltomata QTL mapping

# Mapping raw reads from Novogene to tomato genome build 3.0

###### Checking initial quality of reads with `fastqc`
```
for f in $FILES
do
        if [ "$f" != "rawdata_md5.txt" ]
        then
                fastqc $f
        fi
done
```
Done for all raw read files.

###### Index tomato genome with `BWA`
```
bwa index -a is SLA_3.fa
```

###### Trim and clean reads with `Trimmomatic`
```
for f1 in *-1_1.fq.gz
do
        f2=${f1%%_1.fq.gz}"_2.fq.gz"
        new=$(echo $f2| cut -d'-' -f 1)
        base="Filtered.fq.gz"
        java -Djava.io.tmp.dir=/scratch/ -Xmx1g -jar /N/soft/rhel6/trimmomatic/0.35/trimmomatic-0.35.jar PE $f1 $f2 -baseout ../cleaned/$new$base ILLUMINACLIP:/N/soft/rhel6/trimmomatic/0.35/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:25 MINLEN:36
done
```

###### Check quality post-trimmomatic

```
for f in $FILES
do
        if [ "$f" != "rawdata_md5.txt" ]
        then
                fastqc $f -o 'cleanedQC directory'
        fi
done
```

###### Unzip all trimmed files

```
for f in $FILES
do
        gzip -d $f
done
```
###### Map to tomato assembly 3.0

```
ref='/N/dc2/projects/gibsonTomato/genomes/SLA_3.fa'
for f1 in *_1P.fq
do
        f2=${f1%%_1P.fq}"_2P.fq"
        bwa mem $ref $f1 $f2 -t 32 > $f1-aligned.sam
done
```


## STACKS

###### STACKS `ref_map.pl`
We use the BAM files from mapping to tomato genome as input into STACKS (skipping `process_radtags`)
```
module load gcc/4.9.2
module load stacks

ref_map.pl -m 3 -S -T 15 -b 1 -A 'BC1' \
        -o /N/dc2/projects/gibsonTomato/jaltomata/rawdata/release_data/stacksOutput \
        -p Jsi6Filtered_1P.fq-aligned.sam.bam \
        -p Jum2Filtered_1P.fq-aligned.sam.bam \
        -r ...<all_individual BAM files>...
```

###### STACKS `genotypes.pl` output to JoinMap format
```
module load gcc/4.9.2
module load stacks

genotypes -P /N/dc2/projects/gibsonTomato/jaltomata/rawdata/release_data/stacksOutput \
        -b 1 -r 20 -c -m 6 -t BC1 -o joinmap
```

###### Convert genotypes to R/QTL format using `filter_jp_file.py`



# Linkage Map
###### Build linkage map in R using ASMap.
###### Remove problems markers using `correctGenotypes.py`
See `jaltomataMapping_5.Rmd` for details.

###### Add in trait values

# Map QTL in `R/QTL`
See `QTL_scanning.Rmd` for details

# Candidate gene search
Identifying candidates within QTL regions via blasting marker consensus sequences to tomato.

### Identifying loci in peaks for herm nectar color RGB (for all focal traits)
```
loci <- herm_nec_color_rgb[herm_nec_color_rgb$lod > 2.73,]
loci <- loci[- grep("cL", row.names(a)),]
write.table(loci, sep=",", file="herm_nec_col_RGB.loci")
```

### Gather consensus sequences for these loci
```
python .\getQTLMarkers.py -v -p .\consensus_seq_jalMap_6_17.fq -q .\herm_nec_col_RGB.loci.txt -o .\
```
`consensus_seq_jalMap_6_17.fq` is a fq file with consensus sequences for all loci on the map.
`getQTLMarkers.py` will output fq files for all groups that contain QTL.

### Blast the ITAG CDS database
```
blat /N/dc2/projects/gibsonTomato/genomes/itag_3.2/ITAG3.2_CDS.fasta L.3.consensus.fa output.L3.blast9 -t=
dna -q=dna -out=blast9
```

### Parse blast output
```
python .\parseBlast.py -v -p .\herm_nectar_color_rgb\output.L3.blast9 -o .\herm_nectar_color_rgb\summaryL.3 -t cds -s .\herm_nectar_color_rgb\61.out.txt
 ```

