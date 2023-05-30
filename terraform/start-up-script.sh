#!/bin/bash
echo "Checking for CUDA and installing."
# Check for CUDA and try to install.
# if ! dpkg-query -W cuda-9-0; then
#   # The 16.04 installer works with 16.10.
#   curl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
#   dpkg -i ./cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
#   apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
#   apt-get update
#   apt-get install cuda-9-0 -y
# fi
# if ! dpkg-query -W cuda-10-2; then
#   wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
#   sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
#   wget http://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda-repo-ubuntu1804-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb
#   sudo dpkg -i cuda-repo-ubuntu1804-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb
#   sudo apt-key add /var/cuda-repo-10-2-local-10.2.89-440.33.01/7fa2af80.pub
#   sudo apt update
#   sudo apt -y install cuda-drivers
#   sudo systemctl set-default  multi-user.target
# fi
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

# # add ssh key
# mkdir ~/.ssh

# echo "<ADD_YOUR_SSH_KEY_HERE>"  >> ~/.ssh/id_rsa_gitlab
# ssh-keyscan gitlab.com >>  ~/.ssh/known_hosts
# chmod 0400 ~/.ssh/id_rsa_gitlab
# eval "$(ssh-agent -s)"
# ssh-add ~/.ssh/id_rsa_gitlab


### START THE JUPYTERHUB
# install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone project repository
cd ~
git clone https://github.com/stuart-farris/video_parser

# Enter the jupyterhub directory
cd video_parser/jupyterhub

# build the jupyterhub image
sudo  docker-compose build

# build the notebook image
sudo docker build -t notebook_image Dockerfile.notebook_image

# start the jupyterhub
sudo docker-compose up - d