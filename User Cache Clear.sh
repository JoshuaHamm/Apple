#!/bin/bash

# This clears out user cached items without force closing processes
# This will leave items cached that are currently being utilized by programs to prevent software from closing on the user when remediation runs

# Function to calculate disk space cleared
calculate_space_cleared() {
    local initial_space=$1
    local final_space=$2
    echo $((initial_space - final_space))
}

# Capture initial disk space used
initial_space=$(df / | tail -1 | awk '{print $3}')
echo "Initial disk space used: ${initial_space}K"

# Flush the cache
sudo dscacheutil -flushcache
if [ $? -eq 0 ]; then
    echo "Cache flushed successfully"
else
    echo "Cache flush failed"
fi

# Capture final disk space used
final_space=$(df / | tail -1 | awk '{print $3}')
echo "Final disk space used: ${final_space}K"

# Calculate and echo the disk space cleared
space_cleared=$(calculate_space_cleared $initial_space $final_space)
echo "Disk space cleared: ${space_cleared}K"