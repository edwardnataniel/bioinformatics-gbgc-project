# cpgislands_bed_format.py
# This script converts the CpG islands raw data to BED format.

import os

# Root directory of the project
root_dir = os.path.dirname(os.getcwd()) + "/"

# Path of the raw genes data
dir_in = root_dir + 'raw_data/cpgislands/'

# Path of the output for the trial
dir_out = root_dir + 'trial/00_data/cpgislands/'

# Creates the output folder if it does not exists
if not os.path.exists(dir_out):
    os.makedirs(dir_out)

# Output filename
out_filename = 'cpgislands.txt'

for filename in os.listdir(dir_in):
	fp_in = open(dir_in + filename, 'r')
	fp_out = open(dir_out + out_filename, 'w+')

	lines = []
		
	# Parses the input file and stores it to a list named lines
	for line in fp_in:
		if len(line.strip()) != 0:
			lines.append(line.rstrip().split('\t'))

	# Writes the output to file
	for line in lines:
		fp_out.writelines(str(line[0]) + "\t" + str(line[1]) + "\t" + str(line[2]) + "\n")
