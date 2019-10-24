#! /bin/sh

sudo apt update
sudo apt upgrade -y
sudo apt install build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev libffi-dev
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz && tar xf Python-3.7.0.tar.xz
cd Python-3.7.0
./configure --enable-optimizations && sudo make -j 8
sudo make altinstall
