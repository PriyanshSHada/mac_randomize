#!/bin/bash

# Uninstallation script for MAC Address Randomizer

echo "Uninstalling MAC Address Randomizer..."

# Stop and disable service
sudo systemctl stop mac-randomizer
sudo systemctl disable mac-randomizer

# Remove systemd service
sudo rm -f /etc/systemd/system/mac-randomizer.service
sudo systemctl daemon-reload

# Remove installed files
sudo rm -f /usr/local/bin/mac-randomizer

# Remove log directory
sudo rm -rf /var/log/mac-randomizer

echo "Uninstallation complete. All components removed."