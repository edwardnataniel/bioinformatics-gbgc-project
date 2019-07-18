#!/bin/bash

# bedtools_subtract.sh
# This script subtracts the regions of genes and cpg islands from the hotspots and flanking regions using bedtools.

#SBATCH --qos=shortjobs

# Root directory
root_dir="${PWD%/*}/"

# Directory of the input files
dir_in="${root_dir}trial/01_find_hotspots/"

# Directory of the genes file
dir_genes="${root_dir}trial/00_data/genes/"

# Directory of the CpG islands file
dir_cpgislands="${root_dir}trial/00_data/cpgislands/"

# Path of the output for the trial
dir_out="${root_dir}trial/02_filtered_hotspots/"
mkdir -p $dir_out

hpc bedtools bedtools subtract -a ${dir_in}flanks1.txt -b ${dir_cpgislands}cpgislands.txt -A > ${dir_out}flanks1_minus_cpg.txt
hpc bedtools bedtools subtract -a ${dir_in}flanks2.txt -b ${dir_cpgislands}cpgislands.txt -A > ${dir_out}flanks2_minus_cpg.txt
hpc bedtools bedtools subtract -a ${dir_in}hotspots.txt -b ${dir_cpgislands}cpgislands.txt -A > ${dir_out}hotspots_minus_cpg.txt

hpc bedtools bedtools subtract -a ${dir_out}flanks1_minus_cpg.txt -b ${dir_genes}genes.txt -A > ${dir_out}flanks1_filtered.txt
hpc bedtools bedtools subtract -a ${dir_out}flanks2_minus_cpg.txt -b ${dir_genes}genes.txt -A > ${dir_out}flanks2_filtered.txt
hpc bedtools bedtools subtract -a ${dir_out}hotspots_minus_cpg.txt -b ${dir_genes}genes.txt -A > ${dir_out}hotspots_filtered.txt
