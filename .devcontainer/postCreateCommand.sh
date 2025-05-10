#!/bin/bash

# Install tools specified in mise.toml
#
cd /workspaces/real-time-ml-system-cohort-4
mise trust
mise install
echo 'eval "$(/usr/local/bin/mise activate bash)"' >> ~/.bashrc
source ~/.bashrc

# Install TA-Lib dependencies
echo "Installing TA-Lib..."
# Install build dependencies
apt-get update
apt-get install -y build-essential wget

# Download and install TA-Lib C/C++ library 
wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz
tar -xzf ta-lib-0.6.4-src.tar.gz
cd ta-lib-0.6.4/
./configure --prefix=/usr
make
make install
cd ..

# Create symbolic links for header files in the specific path the Python wrapper is looking for
mkdir -p /usr/include/ta-lib
ln -s /usr/include/ta_*.h /usr/include/ta-lib/
ln -s /usr/include/ta_*_wrappers.h /usr/include/ta-lib/

# Install Python wrapper
pip install ta-lib==0.6.3 --verbose

# Clean up
rm -rf ta-lib-0.6.4 ta-lib-0.6.4-src.tar.gz

echo "TA-Lib installation completed"