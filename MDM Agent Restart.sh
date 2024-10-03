#!/bin/bash
# Checks for the existence of the agent
if [ -f /Library/LaunchDaemons/com.addigy.agent.plist ]; then
    echo "Agent file exists."
    ls -l /Library/LaunchDaemons/com.addigy.agent.plist

    # Modifies the permissions to verify they are correct and can run as root
    sudo chmod 644 /Library/LaunchDaemons/com.addigy.agent.plist
    sudo chown root:wheel /Library/LaunchDaemons/com.addigy.agent.plist

    # Loads the LaunchDaemon
    sudo -s launchctl load /Library/LaunchDaemons/com.addigy.agent.plist
else
    echo "Agent file does not exist."
fi