#!/bin/bash

# Installation script for MAC Address Randomizer

echo "Installing MAC Address Randomizer..."

# Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install it first."
    exit 1
fi

# Create log directory
sudo mkdir -p /var/log/mac-randomizer
sudo chmod 755 /var/log/mac-randomizer

# Copy main script
sudo cp mac_randomizer.py /usr/local/bin/mac-randomizer
sudo chmod 755 /usr/local/bin/mac-randomizer

# Install systemd service
sudo cp mac-randomizer.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable mac-randomizer

echo "Installation complete. Usage:"
echo "sudo systemctl start mac-randomizer"