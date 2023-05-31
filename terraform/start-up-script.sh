#!/bin/bash

# install drivers
while sudo fuser /var/lib/dpkg/lock \
                  /var/lib/apt/lists/lock \
                  /var/cache/apt/archives/lock >/dev/null 2>&1 ; do
  case $i in
    0 ) j="-" ;;
    1 ) j="\\" ;;
    2 ) j="|" ;;
    3 ) j="/" ;;
  esac
  echo -en "\rWaiting for security updates to finish...$j"
  sleep 1
  i=$(((i+1) % 4))
done
echo "Installing Nvidia driver."
sudo /opt/deeplearning/install-driver.sh
echo "Nvidia driver installed."
# Enable persistence mode
nvidia-smi -pm 1

# Install docker
apt-get update
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt-get update
apt-get install -y docker-ce

# Install nvidia-container-runtime
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  tee /etc/apt/sources.list.d/nvidia-docker.list
apt-get update

# Install nvidia-docker2 and reload the Docker daemon configuration
apt-get install -y nvidia-docker2
pkill -SIGHUP dockerd

### START THE JUPYTERHUB
# install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone project repository
git clone https://github.com/stuart-farris/video_parser /app/video_parser

# Enter the jupyterhub directory
cd /app/video_parser/jupyterhub

# build the jupyterhub image
sudo docker-compose build

# build the notebook image
sudo docker build -t notebook_image -f Dockerfile.notebook_image .

# start the jupyterhub
sudo docker-compose up -d