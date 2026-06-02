#!/bin/bash
# This script is used to run the Bramble hardware tests on a Linux system.
# It assumes that the Bramble hardware tests are located in the same directory as this script.

sudo chwd -a
sudo pacman -Sy --noconfirm

if lspci | grep -i nvidia; then
    sudo nvidia-module-loader
fi

echo "HARDWARE_DONE"
