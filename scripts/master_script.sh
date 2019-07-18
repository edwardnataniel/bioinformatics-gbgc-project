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

# Finds the hotspots and flanking regions from the raw data
sh ./bedtools.sh
