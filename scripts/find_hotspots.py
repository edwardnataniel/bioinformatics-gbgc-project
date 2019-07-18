# find_hotspots.py
# This script finds the hotspots and flanking regions from the recombination data.

# Thresholds for hotspots
HOTSPOTS_RATE_MIN = 15 # In cM/MB
HOTSPOTS_LENGTH_MIN = 3000 # In bp

# Thresholds for flanks
FLANKS_RATE_MAX = 3 # In cM/MB
FLANKS_LENGTH_MIN = 3000 # In bp
FLANKS_LENGTH_MAX = 30000 # In bp

# Maximum distance between hotspots and flanks
HOTSPOTS_FLANKS_MAX_DIST = 3000 

# Storing regions as strings
left_flank = []
hotspot = []
right_flank = []

# Lengths
left_flank_length = []
hotspot_length = []
right_flank_length = []

# Total length of sequences
total_flanking = 0
total_hotspot = 0

# For counting the number of hotspots and flanks combinations
region = 0

start = 0 # For the start of each region of interest
end = 0 # For the end of each region of interest
prev_region_flag = 2 # Flag for the previous recombination rate
curr_region_flag = 0 # Flag for the current recombination rate
# -1 for low, 0 for intermediate, 1 for high
				
# Method that assigns a flag for a particular row
def assign_flag(row):
	if float(row[2]) > HOTSPOTS_RATE_MIN: # If recombination rate is high
		flag = 1
	elif float(row[2]) < FLANKS_RATE_MAX: # If recombination rate is low
		flag = -1
	else:
		flag = 0 # If recombination rate is intermediate
	return flag


# Method that saves the start, end, and type of previous region to a list
def save_prev_region(start, end, flag, region_start, region_end, region_type):
	length = end - start
	if flag == -1 or flag == 1:
		if length >= FLANKS_LENGTH_MIN or length >= HOTSPOTS_LENGTH_MIN:
			region_start.append(start)
			region_end.append(end)
			region_type.append(flag)

# Store flank before
def save_hotspots_flanks(region_start, region_end, region_type):
	global total_flanking
	global total_hotspot
	global region

	region += 1
	region_length = region_end[i-1]-region_start[i-1] # Length of region

	if region_length > FLANKS_LENGTH_MAX: # Too long
		region_start[i-1] = region_end[i-1]-3000 # Move start closer

	total_flanking += region_end[i-1]-region_start[i-1] # Counting total length
	left_flank_length.append(region_end[i-1]-region_start[i-1])
	left_flank.append("chr"+str(ctr)+"\t"+str(region_start[i-1])+"\t"+str(region_end[i-1])+"\t"+str(region))
					
	# Store hotspot
	hotspot.append("chr"+str(ctr)+"\t"+str(region_start[i])+"\t"+str(region_end[i])+"\t"+str(region))
	total_hotspot += region_end[i]-region_start[i] # Counting total length
	hotspot_length.append(region_end[i]-region_start[i])
						
	# Store flank after
	region_length = region_end[i+1]-region_start[i+1] # Length of region

	if region_length > FLANKS_LENGTH_MAX: # Too long
		region_end[i+1] = region_start[i+1]+3000 # Move end closer

	right_flank.append("chr"+str(ctr)+"\t"+str(region_start[i+1])+"\t"+str(region_end[i+1])+"\t"+str(region))
	total_flanking += region_end[i+1]-region_start[i+1] # Counting total length
	right_flank_length.append(region_end[i+1]-region_start[i+1])

import os
			
# Root directory of the project
root_dir = os.path.dirname(os.getcwd()) + "/"

# Path of the raw genes data
dir_in = root_dir + 'trial/00_data/recombination/'

# Path of the output for the edited recombination data
dir_out = root_dir + 'trial/01_find_hotspots/'

# Creates the output folder if it does not exists
if not os.path.exists(dir_out):
    os.makedirs(dir_out)
			
for ctr in range(1, 23):
	input_filepath = dir_in + "plink.chr"+str(ctr)+".GRCh38.map" # Path to file

	region_start = [] # List for starts of each region
	region_end = [] # List for ends of each region
	region_type = [] # List for flags of each region

	with open(input_filepath) as f:
		next(f) # Skip first line
		for line in f: # Each line in file
			row_data = line.split(" ", 4)
			curr_region_flag = assign_flag(row_data)
			
			if prev_region_flag != curr_region_flag: # Start new region
				save_prev_region(start, end, prev_region_flag, region_start, region_end, region_type)
				start = int(row_data[1]) # Set start
				prev_region_flag = curr_region_flag # Update flag
			
			end = int(row_data[1]) # New tail end of region
			
		save_prev_region(start, end, prev_region_flag, region_start, region_end, region_type)
		
		for i in range(1, len(region_type)-1): # For all stored values (except first and last since no flanks)
			if region_type[i] == 1: # A hotspot
				# Check nearest flanks
				prev_low_near = region_type[i-1] == -1 and region_start[i]-region_end[i-1] <= HOTSPOTS_FLANKS_MAX_DIST # Previous is low and is near enough
				next_low_near = region_type[i+1] == -1 and region_start[i+1]-region_end[i] <= HOTSPOTS_FLANKS_MAX_DIST # Next is low and is near enough
				if prev_low_near and next_low_near:
					# Store regions
					save_hotspots_flanks(region_start, region_end, region_type)
						
print ("...found: " + str(len(hotspot)) + " hotspots")
print ("...found: " + str(total_flanking) + " bp of flanking regions")
print ("...found: " + str(total_hotspot) + " bp of hotspot regions")

# Writing to files
flanks1 = open(dir_out + "flanks1.txt", "w")
for i in left_flank:
	flanks1.write(i+"\n") 
flanks1.close()
hotspots = open(dir_out + "hotspots.txt", "w")
for i in hotspot:
	hotspots.write(i+"\n") 
hotspots.close()
flanks2 = open(dir_out + "flanks2.txt", "w")
for i in right_flank:
	flanks2.write(i+"\n") 
flanks2.close()
