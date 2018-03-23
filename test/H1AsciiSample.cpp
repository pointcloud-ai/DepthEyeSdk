/*
 * TI Voxel Lib component.
 *
 * Copyright (c) 2014 Texas Instruments Inc.
 */
#include "DepthEyeInterface.h"
 
#include <iomanip>
#include <fstream>
#include <ostream>

#include <thread>
#include <thread>                // std::thread
#include <mutex>                // std::mutex, std::unique_lock
#include <condition_variable>    // std::condition_variable
#include <queue>
#include <unistd.h>
#include <stdlib.h>
#include <iostream>
using namespace Voxel;
using namespace std;

char rawFrameQueue[42496 * 2];
char XYZpointCloutQueue[4800 * sizeof(float) * 4];
PointCloud::DepthEyeSystem depthEyeSys;

int printOutFrameInfo(short *phaseFrame){
	 
    char buffer[(80+1)*(60/2)+1];
    char * out = buffer;
	const short one_meter = static_cast<short>(1.0f);
    short coverage[80] = {};
   	PointCloud::FrameSize fs =  depthEyeSys.getRevolution();
    
    for(int y=0; y<fs.height; ++y)
    {
        for(int x=0; x<fs.width; ++x)
        {
            short depth = phaseFrame[y*80+x]/100;
            if(depth > 0 && depth < 10)
            {
            	 coverage[x] += static_cast<short>(depth);
            }else
            	 coverage[x] = 0;
        }

        if(y%2 == 1){
	        for(short & c : coverage)
	        {
	            *out++ =  " M#@mo*,.."[c/2];
	            c = 0;
	        }
        	*out++ = '\n';
    	}
    }
    *out++ = 0;
    printf("\n%s", buffer);
	return 0;
}

int printOutFrameInfo(float *xyziPointFrame){
	 
	char buffer[(80+1)*(60/2)+1];
    char * out = buffer;
	const uint16_t one_meter = static_cast<uint16_t>(1.0f);
    uint16_t coverage[80] = {};
   	PointCloud::FrameSize fs =  depthEyeSys.getRevolution();
	for(int y=0; y<fs.height; ++y)
    {
        for(int x=0; x<fs.width; ++x)
        {
            float depth = xyziPointFrame[y*80*4+4*x+2];
            if(depth > 0 && depth < 1.0f)
            {
            	 coverage[x] += static_cast<uint16_t>(depth*10);//depth/0.1;
            }else
            	 coverage[x] = 0;
            	
        }

        if(y%2 == 1){
	        for(uint16_t & c : coverage)
	        {
	            *out++ =  " .,*nM#N@mn"[c/2];
	            c = 0;
	        }
        	*out++ = '\n';
    	}
    }
    *out++ = 0;
    printf("\n%s", buffer);
	return 0;
}

void rawdataCallback(DepthCamera &dc, const Frame &frame, DepthCamera::FrameType c) 
{

	const ToFRawFrame *d = dynamic_cast<const ToFRawFrame *>(&frame);

	if(!d)
	{
		std::cout << "Null frame captured? or not of type ToFRawFrame" << std::endl;
		return;
	}
	short phaseFrame[60*80];
	memcpy((char *)phaseFrame, (char *)d->phase(), sizeof(short) * d->size.width * d->size.height);
	//short amplitudeFrame[60*80];
	//memcpy((char *)amplitudeFrame, (char *)d->amplitude(), sizeof(short) * d->size.width * d->size.height);
	//char ambientFrame[60*80];
	//memcpy((char *)ambientFrame, (char *)d->ambient(), sizeof(char) * d->size.width * d->size.height);
	//char flagsFrame[60*80];
	//memcpy((char *)flagsFrame, (char *)d->flags(), sizeof(char) * d->size.width * d->size.height);   
	printOutFrameInfo(phaseFrame);

}

void pointcloudCallback(DepthCamera &dc, const Frame &frame, DepthCamera::FrameType c) 
{
	const XYZIPointCloudFrame *d = dynamic_cast<const XYZIPointCloudFrame *>(&frame);

	if(!d)
	{
		std::cout << "Null frame captured? or not of type XYZIPointCloudFrame" << std::endl;
		return;
	}
	memcpy((char *)XYZpointCloutQueue, (char *)d->points.data(), sizeof(IntensityPoint)*d->points.size());	
	printOutFrameInfo((float*)XYZpointCloutQueue);
}

int main(int argc, char const *argv[])
{
	Voxel::logger.setDefaultLogLevel(LOG_ERROR);

	depthEyeSys.connect();
	//depthEyeSys.enableFilterHDR();
	//depthEyeSys.enableFilterFlyingPixel(500);
	// for 10fps long range option
	//depthEyeSys.setMode(PointCloud::PRICISTION);
	// for 30fps  shor range option
	depthEyeSys.setMode(PointCloud::STANDARD);
	
	depthEyeSys.registerRawDataCallback(rawdataCallback);
	//depthEyeSys.registerPointCloudCallback(pointcloudCallback);
	depthEyeSys.start();
	
	std::cout << "Press any key to quit" << std::endl;
	getchar();
    std::cout << "Stoping DepthEyesSystem" << std::endl;
    depthEyeSys.disconnect();
	depthEyeSys.stop();
	return 0;
}

