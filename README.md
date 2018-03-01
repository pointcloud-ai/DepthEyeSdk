# DepthEyeSdk


Please send mail to sdk@pointcloud.ai. We will reply you asap.

Check or raise issue on [Issue tracking] (https://github.com/pointcloud-ai/DepthEyeSdk/issues)


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

## Caution
1. Make sure you have used the correct profile which name is H1ForSeeed
1. Please don't change the Integration Duty Cycle（intg_time) more than 20% .Otherwise, it is possible to destroy the hardware
1. The Heat sink could be hot when this module is working, please be carefull to avoid scalding your hands
1. Must update profile before you connect module with Windows Voxel Viewer. Detail please refer to 【[Window version Voxel Viewer config setting]( 
https://github.com/pointcloud-ai/DepthEyeSdk/wiki/Window-version-Voxel-Viewer-config-setting)】



## Test Examples
* [Ascii View Example](https://github.com/pointcloud-ai/DepthEyeSdk/tree/master/test)
* [Android Example](https://github.com/pointcloud-ai/DepthEyeSdk_android)

## Voxel Viewer 

* [Simple viewer on Ubuntu](https://github.com/pointcloud-ai/DepthEyeSdk/tree/master/tools)
* [Windows Voxel Viewer]( http://statics3.seeedstudio.com/assets/file/bazaar/product/Windows_Viewer.rar)【[[Must do action before using: Window version Voxel Viewer config setting]( 
https://github.com/pointcloud-ai/DepthEyeSdk/wiki/Window-version-Voxel-Viewer-config-setting)】

* [Voxel Viewer2 for Ubuntu And OSX]( https://github.com/pointcloud-ai/VoxelViewer2)
* [Viewer Quick Start Guide]( http://www.ti.com.cn/cn/lit/ug/sbou157/sbou157.pdf)

![Voxel Viewer Snapshot](https://raw.githubusercontent.com/pointcloud-ai/DepthEyeSdk/master/third_party/images/VoxelViewerSnapshot.jp2)


## Getting started


### 0) Hardware Install

Please add one usb hub with Independent power supply. Then insert the double head USB cable together on the USB hub and connect the usb hub to your PC.


### 1) SET VOXEL_SDK_PATH

To install vim and cmake, please run:

`sudo apt-get install cmake vim `

Please run `# uname -a` to check system platform version first.

|Plateform | SDK Path |
|- | :-: | 
|Ubuntu 14.04 |/third_party/voxelsdk_ubuntu_3.13|
|Ubuntu 16.04 | /third_party/voxelsdk_ubuntu_4.13|
|MacOs | /third_party/voxelsdk_osx|


Modify .bashrc to set environment variables：

`# vim ~/.bashrc`

add below source code to the end of bashrc file：
```
export VOXEL_SDK_PATH="your_directory/third_party/voxelsdk_ubuntu_3.13"
export PATH=$VOXEL_SDK_PATH/lib:$VOXEL_SDK_PATH/bin:$PATH
```

PS：Please remember to replace voxelsdk_ubuntu_3.13 with your system platform.

We need to make above changes come into effect：
 
`# source ~/.bashrc`

Finally, echo the constant to verify ：

`# echo $VOXEL_SDK_PATH`

### 2) SET USB Driver
(For Ubuntu only)
```
sudo cp ./third_party/udev/rules.d/72-DepthEyeH1CDK.rules /etc/udev/rules.d/

sudo chmod a+x /etc/udev/rules.d/72-DepthEyeH1CDK.rules

sudo udevadm control --reload
```

### 3) Make

In the root directory of SDK, run below commands one by one：

```
$ mkdir build

$ cd build/ 

$ cmake ..

$ make 
```

You can get message as below : 

`[100%] Built target H1AsciiSample`

Plug the module and run it:

`./bin/H1AsciiSample`

You can see the result!

![H1AsciiSample's result](https://raw.githubusercontent.com/pointcloud-ai/DepthEyeSdk/master/third_party/images/ascii_depth_data.jpeg)

## Modify Hardware  


You can modify some of the hardware according to the information we provide to meet your needs.
For example, you can reducing power consumption allows the device to use the standard USB interface for power supply without additional power supply.

[Hardware modification Guide](https://github.com/pointcloud-ai/DepthEyeSdk/wiki/Hardware-modification-Guide).



## Common problem

### Lack of power supply

Need to add usb hub. Then insert the double head USB cable together on the USB hub.

## Wiki

Learn more to use DepthEyeSdk at our [wiki](https://github.com/pointcloud-ai/DepthEyeSdk/wiki).