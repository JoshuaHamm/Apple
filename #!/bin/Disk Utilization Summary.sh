#!/bin/bash
# Quick Storage Summary gathers storage information from commonly used directories.
# No Automatic Action Is Taken In This Script

echoOut () {
echo "$(date) $*"
}

# Addigy Download directory size
echoOut "$(du -hs /Library/Addigy/download-cache/downloaded)"

echoOut "Checking for local TimeMachine snapshots"
if [[ "$(tmutil listlocalsnapshots / | grep -c 'com.apple.TimeMachine' )" -gt 0 ]]
    then
        echoOut "Local TimeMachine Snapshots found."
    else
        echoOut "No Local TimeMachine Snapshots."
fi

# Addigy Packages directory size
echoOut "$(du -h -d1 /Library/Addigy/ansible/packages | sort -h -r)"

echoOut "Application Folder size"
echoOut "$(du -h -d1 /Applications | sort -h -r)"

# /Users directory size
echoOut "$(du -h -d1 /users | sort -h -r)"
