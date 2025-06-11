#!/bin/bash
# Simple setup script for Raspberry Pi 5 with Spotpear 2-channel CAN HAT Plus
# Installs required packages and enables CAN interfaces

set -e

sudo apt update
sudo apt install -y python3 python3-pip python3-serial can-utils

# install python-can via pip
pip3 install --user python-can

# enable SPI interface
if ! grep -q '^dtparam=spi=on' /boot/config.txt; then
    echo 'dtparam=spi=on' | sudo tee -a /boot/config.txt
fi

# enable mcp2515 overlays (adjust oscillator and interrupts to your hat)
if ! grep -q '^dtoverlay=mcp2515-can0' /boot/config.txt; then
    sudo tee -a /boot/config.txt <<'EOL'
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
EOL
fi
if ! grep -q '^dtoverlay=mcp2515-can1' /boot/config.txt; then
    sudo tee -a /boot/config.txt <<'EOL'
dtoverlay=mcp2515-can1,oscillator=16000000,interrupt=24
EOL
fi

# load can modules on boot
if ! grep -q '^mcp2515' /etc/modules; then
    echo 'mcp2515' | sudo tee -a /etc/modules
    echo 'can_dev' | sudo tee -a /etc/modules
fi


cat <<'EOL'
Setup complete. Reboot the system to apply changes.
EOL
