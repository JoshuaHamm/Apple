/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE":
 * <hamm.joshua.t@gmail.com> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.   Josh Hamm
 * ----------------------------------------------------------------------------
 */

#!/bin/bash
# Function to calculate disk space cleared
calculate_space_cleared() {
    local initial_space=$1
    local final_space=$2
    echo $((initial_space - final_space))
}

# Capture initial disk space used
initial_space=$(df / | tail -1 | awk '{print $3}')
echo "Initial disk space used: ${initial_space}K"

# Flush user the cache
sudo dscacheutil -flushcache
if [ $? -eq 0 ]; then
    echo "Cache flushed successfully"
else
    echo "Cache flush failed"
fi

# Clear Addigy cached items
if [ -d "/Library/Addigy/download-cache/downloaded" ]; then
    initial_space_addigy=$(du -s /Library/Addigy/download-cache/downloaded | awk '{print $1}')
    rm -Rf /Library/Addigy/download-cache/downloaded/*
    if [ $? -eq 0 ]; then
        final_space_addigy=$(du -s /Library/Addigy/download-cache/downloaded | awk '{print $1}')
        space_cleared_addigy=$(calculate_space_cleared $initial_space_addigy $final_space_addigy)
        echo "Addigy Download Cache Cleared. Disk space cleared: ${space_cleared_addigy}K"
    else
        echo "Failed to clear Addigy Download Cache."
    fi
else
    echo "Addigy Download Cache directory does not exist."
fi

# Capture final disk space used
final_space=$(df / | tail -1 | awk '{print $3}')
echo "Final disk space used: ${final_space}K"

# Calculate and echo the total disk space cleared
space_cleared=$(calculate_space_cleared $initial_space $final_space)
echo "Total disk space cleared: ${space_cleared}K"