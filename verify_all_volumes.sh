#!/bin/bash

# List all disk volumes and extract their identifiers
volumes=$(diskutil list | grep '^/dev/' | awk '{print $1}')

# Iterate through each volume and verify it
for volume in $volumes; 
do 
	echo "Verifying volume: $volume"
	diskutil verifyVolume $volume
done