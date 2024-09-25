#!/bin/bash

# List all disk volumes and extract their identifiers
volumes=$(diskutil list | grep '^/dev/' | awk '{print $1}')

# Iterate through each volume and verify it
for volume in $volumes; 
do 
	echo "Verifying volume: $volume"
	diskutil verifyVolume $volume
	
	# Check if the verifyVolume command failed
	if [ $? -ne 0 ]; then
		echo "Error detected in volume: $volume. Attempting to repair..."
		diskutil repairVolume $volume
	fi
done