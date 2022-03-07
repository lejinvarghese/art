# Generative Art

 `Guided Diffusion: Disco v5`

Just art, because art.

## Plan

1. [Diffusion](docs/disco_diffusion_v5.ipynb)
2. [Spotify + Genius API](https://medium.com/swlh/how-to-leverage-spotify-api-genius-lyrics-for-data-science-tasks-in-python-c36cdfb55cf)
3. [YouTube Downloader](https://www.geeksforgeeks.org/pytube-python-library-download-youtube-videos/)
4. [Video to Image](https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames)
   1. May not be necessary, animated starts maybe possible, re-evaluate


## Concepts

- [ ] Diffusion Models
  - [ ] [Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233)
- [ ] [Self Supervised Learning, Conditional vs Unconditional GANs](https://towardsdatascience.com/self-supervised-gans-2aec1eadaccd)


## Appendix


```bash
virtualenv --python=/usr/bin/python3.10 .venv
source .venv/bin/activate

# if you need cuda dependencies
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

mv ./CLIP ./clip
mv ./ResizeRight ./resize_right
mv ./guided-diffusion ./guided_diffusion
mv ./latent-diffusion ./latent_diffusion
mv ./taming-transformers ./taming_transformers

pip3 install -e ./clip
pip3 install -e ./resize_right
pip3 install -e ./guided_diffusion
pip3 install -e ./latent_diffusion
pip3 install -e ./taming_transformers

# pip3 install --cache-dir=$TMP_DIR torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

```