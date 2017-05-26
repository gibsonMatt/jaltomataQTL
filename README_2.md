# Jaltomata QTL mapping

## Mapping raw reads to tomato genome build 3.0

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

## Variant Calling

###### Convert sam to bam using `Samtools` 1.3

```
for f1 in *.sam
do
        echo $f1
        samtools view -b -S -o ../bamFiles/$f1.bam $f1
done
```

###### Sort bam using `Samtools` 1.3

```
for f1 in *.bam
do
        echo $f1
        samtools sort $f1 ../sorted/$f1.sorted
done
```
###### Index bam files using `Samtools` 1.3

```
for f1 in *.sorted.bam
do
        echo $f1
        samtools index $f1
done
```

###### Pile up and call variants with `Samtools` 1.3 and `bcftools` 1.3

```
samtools mpileup -u -f $ref -b ../fileList.txt > ../variants/variants_all_raw.bcf
bcftools call -c -v  variants/variants_all_raw.bcf > ../variants/variants_all_raw.vcf

#Trying this now...
samtools mpileup --skip-indels -d 250 -t DP -u -f $ref ../fileList.txt > ../variants/variants_4_new_raw.bcf
bcftools call --skip-variants indels -vm ../variants/variants_all_raw.bcf > ../variants/variants_4_new_raw.vcf
```

###### Stats for variant calls pre-filter using `bcftools` 1.3
```
bgzip variants_all_raw.vcf
tabix -p vcf variants_all_raw.vcf.gz

bcftools stats -F {ref.fa} -s - variants_all_raw.vcf.gz > variants_all_raw.vcf.gz.stats
```

###### Filter by quality using `bcftools` 1.3
```
#Not using soft filter. Filtering by QUAL and DEPTH
bcftools filter -O v -o variants_filtered_all_3.vcf -i'QUAL>30 && DP>30 && QUAL<900 && DP<500 && N_ALT<4' variants_all_raw.1.vcf.gz

bcftools filter -O v -o variants_filtered_all_6.vcf -i'AF==0 && AF<99.5 && QUAL>30 && DP>30 && QUAL<900 && DP<500 && N_ALT<4' variants_4_new_raw.vcf
```


###### Convert vcf to HapMap format using custom script
```
python vcf-to-hap.py variants_filtered_all_6.vcf

Produced out.filtered_5.hap
```

###### Identify markers with lots of missing data

I open the initial vcf (post-filter in bcftools) in TASSEL
