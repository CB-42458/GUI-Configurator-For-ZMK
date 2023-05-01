#!/bin/bash
# This shell script is used to setup the packages for the project
# It will install all three of the custom packages in the project
# As well as the libraries which are found in the requirements.txt file
# If you are using a virtual environment, make sure you are in the virtual environment before running this file
pip install -r requirements.txt
# Install the List Union package
cd ./ListUnion
pip install ./
rm -rf ./build
rm -rf ./ListUnion.egg-info
# Install the pykle_serial package
cd ../pykle_serial
pip install ./pykle_serial
rm -rf ./build
rm -rf ./pykle_serial.egg-info
# Install the ZMK package
cd ../ZMK
pip install ./ZMK
rm -rf ./build
rm -rf ./ZMK.egg-info
cd ..