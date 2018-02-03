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

## Getting started

Learn more to use DepthEyeSdk at our [wiki](https://github.com/pointcloud-ai/DepthEyeSdk/wiki)


### 1) SET VOXEL_SDK_PATH


|Plateform | SDK Path |
|- | :-: | 
|Ubuntu 14.04 |/third_party/voxelsdk_ubuntu_3.13|
|Ubuntu 16.04 | /third_party/voxelsdk_ubuntu_4.13|
|MacOs | /third_party/voxelsdk_osx|
 

Modify .bashrc to add SDK path：

`# vi /etc/profile`

`export VOXEL_SDK_PATH ="your_directory/third_party/voxelsdk_ubuntu_3.13"`

 
`# source /etc/profile`

`# echo $VOXEL_SDK_PATH `

### 2) SET USB Driver
(For Ubuntu only)

`cp /third_party./udev/rules.d/72-DepthEyeH1CDK.rules /etc/udev/rules.d/`

`chmod a+x /etc/udev/rules.d/72-DepthEyeH1CDK.rules`

### 3) Make

`$ mkdir build    `

`$ cd build/   `

`$ cmake ..`

`$ make ..`

You can get message as below : 

`[100%] Built target H1AsciiSample`

Plug the module and run it:

`./bin/H1AsciiSample`

You can see the result!
