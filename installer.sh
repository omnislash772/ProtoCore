#!/bin/bash

if [ $(id -u) -ne 0 ]; then
	echo "Installer must be run as root."
	echo "Try 'sudo bash $0'"
	exit 1
fi
echo "Script made by @DrekkTheProto"

echo "Installing dependiencies"
apt update
apt install -y --force-yes libbluetooth-dev python3-pip libportaudio2
python3 -m pip install -r requirements.txt
echo "Downloading adafruit setup script"
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh > rgb-matrix.sh
echo "If you're using the default bonnet, you want to use the \"Convenience\" setting"
echo "Running installer script, make sure you reboot afterwards"
echo "When the reboot is done, run the Proto.py script for protogen"
source rgb-matrix.sh