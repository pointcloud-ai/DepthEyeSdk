#ifndef POINTCLOUD_DEPTHEYE_H
#define POINTCLOUD_DEPTHEYE_H
#include "CameraSystem.h"
#include "Common.h"
namespace PointCloud
{
	enum DEPTH_MODE{
		UNKNOWN_MODE = 0,
		STANDARD,
		PRICISTION
	};

	enum DEVICE_STATUS
	{
		UNKNOWN_STATUS = 0,
		INITIALIZED,
		CONNECTED,
		STARTED,
		STOP
	};

	struct FrameSize
	{
	  uint32_t width, height;
	};

	class DepthEyeSystem
	{
	public:
		DepthEyeSystem();
		DepthEyeSystem(int vid,int pid);
		DepthEyeSystem(int vid,int pid,std::string&  usbFd);
		void setMode(DEPTH_MODE mode);
		DEVICE_STATUS connect();
		bool isInitialiszed(DEPTH_MODE mode);
		bool enableFilterHDR();
		bool enableFilterFlyingPixel(int threshold);
		void registerPointCloudCallback(Voxel::DepthCamera::CallbackType f);
		void registerRawDataCallback(Voxel::DepthCamera::CallbackType f);
		bool start();
		void stop();
		void reset();
		bool disconnect();
		float  getFrameRate();
		float  getFOV();
		FrameSize  getRevolution();
	private:
		Voxel::CameraSystem	  cameraSys_;
		Voxel::DepthCameraPtr depthCamera_;
		Voxel::DevicePtr 	  device_;
		DEPTH_MODE 			  mode_;
		DEVICE_STATUS 		  status_;

		Voxel::DepthCamera::CallbackType pontcloud_func_;
		Voxel::DepthCamera::CallbackType rawdata_func_;
	};
}
#endif