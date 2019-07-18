#!/bin/bash

# download_sequences.sh
# This script downloads the sequences data corresponding to the hotspots and their flanking regions from the 1000 Genomes Project Repository

## PARAMETERS
#SBATCH --qos=shortjobs
#SBATCH --job-name=ParallelFilteredGetter.sh
#SBATCH --ntasks=1

# Root directory
root_dir="${PWD%/*}/"

# Directory of the input files
dir_in="${root_dir}trial/02_filtered_hotspots/"

# Directory of the f1 output files
dir_f1_out="${root_dir}trial/03_vcf_files/f1/"
mkdir -p $dir_f1_out

# Directory of the hoy output files
dir_h_out="${root_dir}trial/03_vcf_files/hotspots/"
mkdir -p $dir_h_out

# Directory of the f1 output files
dir_f2_out="${root_dir}trial/03_vcf_files/f2/"
mkdir -p $dir_f2_out

{
while read -r f1_chrom f1_start f1_end f1_name h_chrom h_start h_end h_name f2_chrom f2_start f2_end f2_name
do
	# Gets the chromosome number from the string
	chrom_num=$(echo $h_chrom | cut -c 4-)
	
	# Downloads the left flanks data
	echo "...downloading $f1_chrom f1 $f1_name"
  	hpc htslib tabix -h -p vcf -f ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/ALL.${f1_chrom}_GRCh38.genotypes.20170504.vcf.gz ${chrom_num}:${f1_start}-${f1_end} > ${dir_f1_out}f1_${f1_name}.vcf

	# Downloads the hotspots data
	echo "...downloading $h_chrom hotspots $h_name"
  hpc htslib tabix -h -p vcf -f ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/ALL.${h_chrom}_GRCh38.genotypes.20170504.vcf.gz ${chrom_num}:${h_start}-${h_end} > ${dir_h_out}h_${h_name}.vcf

	# Downloads the right flanks data
	echo "...downloading $f2_chrom f2 $f2_name"
  hpc htslib tabix -h -p vcf -f ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/ALL.${f2_chrom}_GRCh38.genotypes.20170504.vcf.gz ${chrom_num}:${f2_start}-${f2_end} > ${dir_f2_out}f2_${f2_name}.vcf

done
} < "${dir_in}/combined_bed.txt"
