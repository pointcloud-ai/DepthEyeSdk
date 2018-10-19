###
# PointCloud Python Sample : ShowDepthNoGUI.
#
# Copyright (c) 2018 PointCloud.AI Inc.
#
# Author : Adam.Han
#
# Functional description:
#    Show simple usage with python to get depth information from DepthEye Camera
# 
# Exit shortcut keys:
#     Input [Enter] Key
###

import Voxel
import numpy as np

def createWindow():
    global window
    if window == None:
        window = MainWindow(cameraSystem)
    return

class MainWindow():
   
    def __init__(self, cameraSystem):
        print("MainWindow init")
        self.depthCamera = cameraSystem.connect(devices[0])
        self.data = {}
        if self.depthCamera:
            self.depthCamera.clearAllCallbacks()
            self.depthCamera.registerCallback(Voxel.DepthCamera.FRAME_DEPTH_FRAME, self.processDepthFrame)
            self.depthCamera.registerCallback(Voxel.DepthCamera.FRAME_XYZI_POINT_CLOUD_FRAME, self.processPointCloudFrame)
            if not self.depthCamera.start():
                print(" start fail")
            else:
                print(" start ok")

    def processDepthFrame(self, depthCamera, frame, type):
        #frame = self.depthQueue.get(timeout=0.25)

        if frame is None:
            return

        depthFrame = Voxel.DepthFrame.typeCast(frame)

        if not depthFrame:
            return

        d = np.array(depthFrame.depth)
        d1 = np.transpose(d.reshape((depthFrame.size.height, depthFrame.size.width)))
        print("point(x:40,y:30)'s distance is %s  meter." %d1[40][30])

    def processPointCloudFrame(self, depthCamera, frame, type):

        if frame is None:
            return

        pointCloudFrame = Voxel.XYZIPointCloudFrame.typeCast(frame)

        if not pointCloudFrame:
            return

        pcf = np.array(pointCloudFrame, copy=True)

        print("pointCloudFrame.size:  %s" %pointCloudFrame.size())

        ###  point.i is intensity, which come from amplitude
        ###  point.z is distance, which come from depth

        # for index in range(pointCloudFrame.size()):
        #     point = pointCloudFrame.points[index]
        #     print("current point : index %s  [ x : %s , y: %s ,z : %s ,i : %s]" %(index, point.x,point.y,point.z,point.i))
    
    def stop(self):
        if self.depthCamera:
            self.depthCamera.stop()
            self.depthCamera.clearAllCallbacks()
            del self.depthCamera
            self.depthCamera = None

cameraSystem = Voxel.CameraSystem()

devices = cameraSystem.scan()

if len(devices) == 1:
    print(" Find one device.")
    window = MainWindow(cameraSystem)
    key = raw_input("Input enter key to quit.")
    print(" Quit now.")
    window.stop()
else:
    print(" No device found.")

del cameraSystem


