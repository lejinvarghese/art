# AI Generative Art

 `Guided Diffusion: vDisco`

Just art because is art.

## Activate

```bash
virtualenv --python=/usr/bin/python3.10 .venv
source .venv/bin/activate

# wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
# sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
# wget https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda-repo-ubuntu2004-11-6-local_11.6.1-510.47.03-1_amd64.deb
# sudo dpkg -i cuda-repo-ubuntu2004-11-6-local_11.6.1-510.47.03-1_amd64.deb
# sudo apt-key add /var/cuda-repo-ubuntu2004-11-6-local/7fa2af80.pub
# sudo apt-get update
# sudo apt-get -y install cuda


sudo apt install imagemagick
pip3 install -r requirements.txt

git clone https://github.com/openai/CLIP
git clone https://github.com/crowsonkb/guided-diffusion
git clone https://github.com/assafshocher/ResizeRight.git
git clone https://github.com/CompVis/latent-diffusion.git
git clone https://github.com/CompVis/taming-transformers

pip install -e ./CLIP
pip install -e ./guided-diffusion
pip install -e ./taming-transformers
pip install opencv-python
pip install matplotlib

mv ./CLIP ./clip
mv ./ResizeRight ./resize_right
mv ./guided-diffusion ./guided_diffusion
mv ./latent-diffusion ./latent_diffusion
mv ./taming-transformers ./taming_transformers
```