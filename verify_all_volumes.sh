#!/bin/bash

# List all disk volumes and extract their identifiers
volumes=$(diskutil list | grep '^/dev/' | awk '{print $1}')

# Iterate through each volume and verify it
for volume in $volumes; 
do 
	# Get the volume description
	description=$(diskutil info $volume | grep 'Volume Name' | awk -F: '{print $2}' | xargs)
	
	# Skip volumes associated with .dmg files
	if [[ $description == *.dmg* ]]; then
		echo "Skipping volume: $volume (associated with .dmg file)"
		continue
	fi
	
	echo "Verifying volume: $volume"
	diskutil verifyVolume $volume
	
	# Check if the verifyVolume command failed
	if [ $? -ne 0 ]; then
		echo "Error detected in volume: $volume. Attempting to repair..."
		diskutil repairVolume $volume
		
		# Check if the repairVolume command failed
		if [ $? -ne 0 ]; then
			echo "Repair failed for volume: $volume. Errors are still present."
		else
			echo "Repair successful for volume: $volume."
		fi
	fi
done