#!/bin/bash

# Computes the recombination rates of the raw data
echo 'Computing recombination rates:'
python3 compute_recombination.py

# Converts the genes raw data to BED format
echo 'Converting genes raw data to BED format...'
python3 genes_bed_format.py

# Converts the cpgislands raw data to BED format
echo 'Converting cpg islands raw data to BED format...'
python3 cpgislands_bed_format.py

# Finds the hotspots and flanking regions from the raw data
echo 'Finding the hotspots and flanking regions...'
python3 find_hotspots.py

# Subtract the positions of genes and cpg islands from the hotspots and flanking regions
sh ./bedtools_subtract.sh

# Combines the hotspots with their corresponding left and right flanks
python3 combine_script.py

# Downloads the sequences data corresponding to the hotspots and their flanking regions from the 1000 Genomes Project Repository
sh ./download_sequences.sh
