virtualenv --python=/usr/bin/python3.10 .venv
source .venv/bin/activate

# if you need cuda dependencies
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda-repo-ubuntu2004-11-6-local_11.6.1-510.47.03-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2004-11-6-local_11.6.1-510.47.03-1_amd64.deb
sudo apt-key add /var/cuda-repo-ubuntu2004-11-6-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda


sudo apt install imagemagick
pip3 install -r requirements.txt

git clone https://github.com/openai/CLIP
git clone https://github.com/crowsonkb/guided-diffusion
git clone https://github.com/assafshocher/ResizeRight.git

git clone https://github.com/facebookresearch/SLIP.git

git clone https://github.com/CompVis/latent-diffusion.git
git clone https://github.com/CompVis/taming-transformers

# python3 setup.py install develop

pip3 install -e ./CLIP
pip3 install -e ./ResizeRight
pip3 install -e ./guided-diffusion
pip3 install -e ./latent-diffusion
pip3 install -e ./taming-transformers

pip3 install --cache-dir=$TMP_DIR torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html