#!/bin/bash

# Update system package list
echo "Updating system package list..."
sudo apt-get update -y

# Install required dependencies
echo "Installing required dependencies..."
sudo apt-get install -y build-essential cmake git

# Clone CuraEngine source code from GitHub
echo "Cloning CuraEngine repository..."
git clone https://github.com/Ultimaker/CuraEngine.git
cd CuraEngine

# Create a build directory
echo "Creating build directory..."
mkdir build
cd build

# Build CuraEngine from source
echo "Building CuraEngine..."
cmake ..
make

# Test if CuraEngine was installed successfully
echo "Testing CuraEngine installation..."
./curaengine --version

echo "CuraEngine installation completed!"
