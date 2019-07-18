# combine_script.py
# This script combines the hotspots with their corresponding left and right flanks
 
import os

# Root directory of the project
root_dir = os.path.dirname(os.getcwd()) + "/"

# Path of the input files
dir_in = root_dir + 'trial/02_filtered_hotspots/'

# Input files
flanks1 = open(dir_in + 'flanks1_filtered.txt')
flanks2 = open(dir_in +'flanks2_filtered.txt')
hotspots = open(dir_in +'hotspots_filtered.txt')

# Path of the output of the combined 
dir_out = dir_in

# Output file
combined_bed = open(dir_out + 'combined_bed.txt', 'w')

# Contains the id/names of the input regions
flanks1list = []
flanks2list = []
hotspotslist= []

# Contains all the columns of the BED file
flanks1_col1to4 = []
flanks2_col1to4 = []
hotspots_col1to4 = []

# Contains the id/names of remaining regions after intersection
flanks1_filtered = []
flanks2_filtered = []
hotspots_filtered = []

# Saves the columns of the left flanks BED file into a list
for line in flanks1:
	flanks1_line = [x.strip() for x in line.split('\t')]
	flanks1_col4 = int(flanks1_line[3])
	flanks1list.append(flanks1_col4)
	flanks1_col1to4.append(flanks1_line)

# Saves the columns of the right flanks BED file into a list
for line in flanks2:
	flanks2_line = [x.strip() for x in line.split('\t')]
	flanks2_col4 = int(flanks2_line[3])
	flanks2list.append(flanks2_col4)
	flanks2_col1to4.append(flanks2_line)

# Saves the columns of the hotspots BED file into a list
for line in hotspots:
	hotspots_line = [x.strip() for x in line.split('\t')]
	hotspots_col4 = int(hotspots_line[3])
	hotspotslist.append(hotspots_col4)
	hotspots_col1to4.append(hotspots_line)

# Gets the common id/names in the lists
combinedflanks = list(set(flanks1list).intersection(flanks2list))
combined = list(set(combinedflanks).intersection(hotspotslist))

# Saves the rows corresponding to the filtered id/names
for x in flanks1_col1to4:
	if int(x[3].rstrip()) in combined:
		flanks1_filtered.append(x)

# Saves the rows corresponding to the filtered id/names
for x in hotspots_col1to4:
	if int(x[3].rstrip()) in combined:
		flanks2_filtered.append(x)

# Saves the rows corresponding to the filtered id/names
for x in flanks2_col1to4:
	if int(x[3].rstrip()) in combined:
		hotspots_filtered.append(x)

# Outputs the left flank, hotspots, and right flanks to a file
for i in range(0, len(flanks1_filtered)):
	combined_bed.write("\t".join(flanks1_filtered[i]) + " " + "\t".join(flanks2_filtered[i]) + " " + "\t".join(hotspots_filtered[i]) + '\n')
