# compute_recombination.py
# This script computes the recombination rate of each region (in cM/MB) in the recombination data.

import os

# Root directory of the project
root_dir = os.path.dirname(os.getcwd()) + "/"

# Path of the raw recombination data
dir_in = root_dir + '/raw_data/recombination/'

# Path of the output for the edited recombination data
dir_out = root_dir + 'trial/00_data/recombination/'

# Creates the output folder if it does not exists
if not os.path.exists(dir_out):
    os.makedirs(dir_out)

# File extension of input and output files
file_type = '.map'

# Indices of cM and MB in the input file
cm_index = 2
mb_index = 3

# Header row of the output file
header_out = 'Chromosome Position(bp) Rate(cM/Mb) Map(cM)\n'

for filename in os.listdir(dir_in):
	if filename.endswith(file_type):
		print('...' + filename)

		fp_in = open(dir_in + filename, 'r')
		fp_out = open(dir_out + filename, 'w+')

		lines = []
		
		# Parses the input file and stores it to a list named lines
		for line in fp_in:
			lines.append(line.rstrip().split(' ')) 

		num_lines = len(lines)
		
		# Computes the recombination rate per row and appends it to the list
		for i in range(0, num_lines):
			if i != num_lines-1:
				diff_cM = float(lines[i+1][cm_index]) - float(lines[i][cm_index])
				diff_MB = (float(lines[i+1][mb_index]) - float(lines[i][mb_index]))/1000000
				lines[i].append(str(diff_cM / diff_MB))
			else:
				# Recombination rate of last row is 0
				lines[num_lines-1].append('0')
		
		# Writes the header line to output
		fp_out.writelines(header_out)
		
		# Writes the output to file
		for line in lines:
			new_order = [0, 3, 4, 2] # Reorders the columns
			line = [line[i] for i in new_order]
			fp_out.writelines(' '.join(line) + '\n')
