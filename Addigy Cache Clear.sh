!/bin/bash
# Cleans out Addigy cached items
# Function to calculate disk space cleared
calculate_space_cleared() {
    local initial_space=$1
    local final_space=$2
    echo $((initial_space - final_space))
}

# Clear Addigy Download Cache
if [ -d "/Library/Addigy/download-cache/downloaded" ]; then
    initial_space=$(du -s /Library/Addigy/download-cache/downloaded | awk '{print $1}')
    rm -Rf /Library/Addigy/download-cache/downloaded/*
    if [ $? -eq 0 ]; then
        final_space=$(du -s /Library/Addigy/download-cache/downloaded | awk '{print $1}')
        space_cleared=$(calculate_space_cleared $initial_space $final_space)
        echo "Addigy Download Cache Cleared. Disk space cleared: ${space_cleared}K"
    else
        echo "Failed to clear Addigy Download Cache."
    fi
else
    echo "Addigy Download Cache directory does not exist."
fi