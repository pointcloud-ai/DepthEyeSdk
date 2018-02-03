#include "DepthEyeInterface.h"
namespace PointCloud
{
	using namespace Voxel;
	DepthEyeSystem::DepthEyeSystem()
	{
		//logger.setDefaultLogLevel(LOG_INFO);
		
		// Get all valid detected devices
		const Vector<DevicePtr> &devices = cameraSys_.scan();
		bool found = false;
		for (auto &d: devices){
			logger(LOG_INFO) <<  "Detected devices: "  << d->id() << std::endl;
			device_ = d;
			found = true;
		}
		if(found)
			status_ = INITIALIZED;
		else
			status_ = UNKNOWN_STATUS;

		if(!found)
		{
			logger(LOG_ERROR) << "Find depth camera FAILED " << std::endl;
			return;
		}
		logger(LOG_CRITICAL) << "Successfully init depth camera for device: " << device_->id() << std::endl;
	}

	DepthEyeSystem::DepthEyeSystem(int vid,int pid)
	{
		//device_ = DevicePtr(new USBDevice(0x0451, 0x9107, "1025594", -1, "", ""));
		std::string usbFd = "1025594";
		DepthEyeSystem(vid,pid,usbFd);
	}

	DepthEyeSystem::DepthEyeSystem(int vid,int pid,std::string&  usbFd)
	{
		device_ = DevicePtr(new USBDevice(vid, pid, usbFd, -1, "", ""));
		logger(LOG_INFO) << "simulate USB devices: VID:" << vid << " PID: " << pid << " Serial:" << usbFd <<std::endl;

		if (!device_) {
			status_ = UNKNOWN_STATUS;
			logger(LOG_ERROR)
					<< "No valid device found for the specified VID:PID:serialnumber"
					<< std::endl;
			return ;
		}

		logger(LOG_CRITICAL) << "Successfully init depth camera for device: " << device_->id() << std::endl;
		status_ = INITIALIZED;
	}

	void DepthEyeSystem::setMode(DEPTH_MODE mode)
	{
		if(status_ != CONNECTED)
			return;

		FrameRate r;
		uint32_t intg_duty_cycle = 20;
		if(mode == STANDARD)
		{
		  intg_duty_cycle = 20;
		  r.numerator = 30;
		  r.denominator = 1;
		
		}else if(mode == PRICISTION)
		{
		  intg_duty_cycle = 30;
		  r.numerator = 10;
		  r.denominator = 1;
		}

		depthCamera_->setFrameRate(r);
		depthCamera_->set("intg_duty_cycle",intg_duty_cycle );
    	logger(LOG_INFO) << "Successfully set mode: " << mode << " intg_duty_cycle:" <<  intg_duty_cycle << " fps:" << r.numerator<< std::endl;
		mode_ = mode;
	}

	DEVICE_STATUS DepthEyeSystem::connect()
	{
		if(status_ != INITIALIZED)
			return status_;

		if(status_ == CONNECTED)
			return status_;

		depthCamera_ = cameraSys_.connect(device_);
		if (!depthCamera_) {
			logger(LOG_ERROR) << "Could not load depth camera for device "<< device_->id() << std::endl;
			return status_;
		}

		if (!depthCamera_->isInitialized()) {
			logger(LOG_ERROR) << "Depth camera not initialized for device "<< device_->id() << std::endl;
			return status_;
		}

		unsigned int scratch1 = 0;
		bool scratch1_value = depthCamera_->get("scratch1", scratch1, true);
		depthCamera_->set("stanby", true);
		if (scratch1_value &&scratch1>0)
		{
			logger(LOG_INFO) << "reseting camera"<< std::endl;
			depthCamera_->stop();
			depthCamera_->reset();
			cameraSys_.disconnect(depthCamera_);
			depthCamera_ = nullptr;
			depthCamera_ = cameraSys_.connect(device_);
			depthCamera_->refreshParams();
		}

		status_ = CONNECTED;
		logger(LOG_CRITICAL) << "Successfully Connect to depth camera for device: " << device_->id() << std::endl;
		return status_;
	}

	bool DepthEyeSystem::isInitialiszed(DEPTH_MODE mode)
	{
		if(mode == mode_)
			return true;
		else
			return false;
	}

	bool DepthEyeSystem::enableFilterHDR()
	{
		if(status_ != CONNECTED)
			return false;

		FilterPtr p = cameraSys_.createFilter("Voxel::HDRFilter",
										DepthCamera::FRAME_RAW_FRAME_PROCESSED);
		if (!p) {
			logger(LOG_ERROR) << "Failed to get HDRFilter" << std::endl;
			return false;
		}
		depthCamera_->addFilter(p, DepthCamera::FRAME_RAW_FRAME_PROCESSED);
		logger(LOG_INFO) << "Successfully enableFilterHDR "<< std::endl;	
		return true;
	}

	bool DepthEyeSystem::enableFilterFlyingPixel(int threshold)
	{
		if(status_ != CONNECTED)
			return false;

		FilterPtr p = cameraSys_.createFilter("Voxel::FlypixFilter",
										DepthCamera::FRAME_RAW_FRAME_PROCESSED);
	    if (!p) {
	      logger(LOG_ERROR) << "Failed to get FlypixFilter" << std::endl;
	      return false;
	    }
	    p->set("threshold", threshold);

	    depthCamera_->addFilter(p, DepthCamera::FRAME_RAW_FRAME_PROCESSED);

	    logger(LOG_INFO) << "Successfully enableFilterFlyingPixel threshold:" <<  threshold << std::endl;
		return true;
	}

	void DepthEyeSystem::registerPointCloudCallback(Voxel::DepthCamera::CallbackType f)
	{
		if(status_ != CONNECTED)
			return ;

		depthCamera_->registerCallback(DepthCamera::FRAME_XYZI_POINT_CLOUD_FRAME,f);
	}

	void DepthEyeSystem::registerRawDataCallback(Voxel::DepthCamera::CallbackType f)
	{
		if(status_ != CONNECTED)
			return ;

		depthCamera_->registerCallback(DepthCamera::FRAME_RAW_FRAME_PROCESSED,f);
	}

	bool DepthEyeSystem::start()
	{
		if(status_ != CONNECTED)
			return false;

		FrameRate r;
		if (depthCamera_->start()) {
			if (depthCamera_->getFrameRate(r)){
				logger(LOG_CRITICAL) << "Start capturing at a frame rate of "<< r.getFrameRate() << " fps" << std::endl;
			}
			status_ = STARTED;
		//	depthCamera_->wait();
		} 
		else
		{
			return false;
			logger(LOG_ERROR) << "Could not start the depth camera "<< depthCamera_->id() << std::endl;
		}
		return true;
	}

	void DepthEyeSystem::stop()
	{
		if(status_ != STARTED)
			return;
		depthCamera_->stop();
	}

	void DepthEyeSystem::reset()
	{
		if(status_ < INITIALIZED)
			return ;
		depthCamera_->reset();
	}
	
	bool DepthEyeSystem::disconnect()
	{
		if(status_ != CONNECTED)
			return false;
		depthCamera_->reset();
		cameraSys_.disconnect(depthCamera_);
		return true;
	}

	float DepthEyeSystem::getFrameRate()
	{
		if(status_ < CONNECTED)
			return (float)0.;

		Voxel::FrameRate fr;
		depthCamera_->getFrameRate(fr);
		return fr.getFrameRate();
	}

	float DepthEyeSystem::getFOV()
	{
		if(status_ < CONNECTED)
			return (float)0.;
		
		float fov;
		depthCamera_->getFieldOfView(fov);
		return fov;
	}

	FrameSize DepthEyeSystem::getRevolution()
	{
		FrameSize fs;
		if(status_ < CONNECTED)
			return fs;
		
		Voxel::FrameSize voxelFs;
		depthCamera_->getFrameSize(voxelFs);
		fs.width = voxelFs.width;
		fs.height = voxelFs.height;
		return fs;
	}
}