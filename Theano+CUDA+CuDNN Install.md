# Note About How to Install CUDA 8.0, CuDNN for Theano on Ubuntu Linux
[1st version, 12-12-2016]

Recently I've got a brand-new machine learning server with Nvidia Tesla M40s installed. The machine comes with Ubuntu 14.04 and CUDA-8.0 pre-installed, however, the pre-installed CUDA does not work, so I've to re-install the underlining drivers and tool chains manually. After two days I realized this is NOT AN EASY PROBLEM. In the following I kept the note of how to install CUDA, CuDNN and configure them to work with Theano, my favorite deep learning library. Hope this will help keep you away from all the pitfalls I've ever met.

## Step I: Remove Previously Installed CUDA and Nvidia Drivers
This is maybe the most important step before you start any installing process. Otherwise you may be trapped in the "An NVIDIA kernel module 'nvidia-drm' appears to already be loaded in your kernel" myth. I hate to say it but this problem cost almost two days. To remove pre-installed Nvidia drivers and CUDA, follow the steps:
  * Remove the current drivers: `sudo apt-get purge nvidia-cuda*`
  * (optional) - If you want to install the drivers too, then run: `sudo apt-get purge nvidia-*`
  * Stop lightdm: `sudo service lightdm stop`

[Ref: http://askubuntu.com/questions/830916/how-to-install-cuda-8-0-on-ubuntu-16-04-with-nvidia-geforce-gtx-1080/842404]

## Step II: Install CUDA
I have to say Nvidia is trying to make this process easier, however that's exactly where the pitfall is. To install the CUDA, make sure you choose the local installer package (*.run), NEVER USE THE WEB INSTALLER. The reason I insist this is because during my first attempts to install CUDA using the web installer, the installed nvcc was weirdly not compatible with the lib files in 'lib64' folder. The problem disappeared when I switched to a local installer.
   * Download the locla installer cuda_8.0.44_linux.run from https://developer.nvidia.com/cuda-downloads
   * Install CUDA by `sudo sh cuda_8.0.44_linux.run`
   * Set path in your enviroment. Edit your .bashrc file, add 
   ```
   export CUDA_ROOT=/usr/local/cuda-8.0
   export PATH=$PATH:/usr/local/cuda-8.0/bin
   export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64:$LD_LIBRARY_PATH
   export LIBRARY_PATH=/usr/local/cuda-8.0:$LIBRARY_PATH
   export CPATH=/usr/local/cuda-8.0/include:$CPATH
   ```

## Step III: Install CuDNN
You have to keep in mind that CUDA does not come along with CuDNN, you have to install it by yourself. To install CuDNN, 
   * Download CuDNN library from https://developer.nvidia.com/rdp/cudnn-download
   * Untar the downloaded archive, there will be a folder named as 'cuda' with two subfolders: 'include' and 'lib64'. Copy everything in 'include' folder to `/usr/local/cuda/include`, and everything in 'lib64' folder to `/usr/local/cuda/lib64`

## Step IV: Install CNMeM
CNMeM is a library to help the Deep Learning frameworks manage CUDA memory. To install this:
   * Download CNMeM from https://github.com/NVIDIA/cnmem
   * Build CNMeM by 
   ```
   % cd cnmem
   % mkdir build
   % cd build
   % cmake ..
   % make
   ```
   * Copy include/cnmem.h to `/usr/local/cuda/include`, any *.so file in build folder to `/usr/local/cuda/lib64`
   * To enable usage CNMeM in Theano, set environment flag as 'lib.cnmem=1'

Now install Theano, and you should have your code run on GPU & CuDNN now.