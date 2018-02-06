# DepthEyeSdk


## Purpose
DepthEyeSdk is a sdk that provides interfaces for Depth Eye.

The Depth Eye is the cost-effective TOF base depth camera. It use TI opt8320 sensor and pass all depth data including pointcloud via USB cable.

Feature:
* Amazing tiny size
* USB 2.0 interface
* Provide Pointcloud  and RAW depth data 
* FOV（D* H*V ） ：90 * 75 * 59
* 2 850nm band infrared LED
* F/NO. is 1.09 
* TI OPT8320 sensor
* Resolution is 80*60

## Sample
[Sample](https://github.com/pointcloud-ai/DepthEyeSdk/tree/master/test)


## Viewer 

* [Simple viewer on Ubuntu](https://github.com/pointcloud-ai/DepthEyeSdk/tree/master/tools)
* [Windows Voxel Viewer]( http://statics3.seeedstudio.com/assets/file/bazaar/product/Windows_Viewer.rar)
* [Viewer Quick Start Guide]( http://www.ti.com.cn/cn/lit/ug/sbou157/sbou157.pdf)


## Getting started

Learn more to use DepthEyeSdk at our [wiki](https://github.com/pointcloud-ai/DepthEyeSdk/wiki)


### 1) SET VOXEL_SDK_PATH

Install 
`sudo apt-get install cmake vim `

|Plateform | SDK Path |
|- | :-: | 
|Ubuntu 14.04 |/third_party/voxelsdk_ubuntu_3.13|
|Ubuntu 16.04 | /third_party/voxelsdk_ubuntu_4.13|
|MacOs | /third_party/voxelsdk_osx|
 

Modify .bashrc to add SDK path：

`# vim ~/.bashrc`

add below source code to the end of bashrc file：

`export VOXEL_SDK_PATH="your_directory/third_party/voxelsdk_ubuntu_3.13"`

We need to make above changes come into effect：
 
`# source ~/.bashrc`

Finally, echo the constant to verify ：

`# echo $VOXEL_SDK_PATH `

### 2) SET USB Driver
(For Ubuntu only)

`sudo cp ./third_party/udev/rules.d/72-DepthEyeH1CDK.rules /etc/udev/rules.d/`

`sudo chmod a+x /etc/udev/rules.d/72-DepthEyeH1CDK.rules`

`sudo udevadm control --reload`

### 3) Make

`$ mkdir build    `

`$ cd build/   `

`$ cmake ..`

`$ make `

You can get message as below : 

`[100%] Built target H1AsciiSample`

Plug the module and run it:

`./bin/H1AsciiSample`

You can see the result!
