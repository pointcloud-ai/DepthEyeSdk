#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

import numpy as np
import math
import pyqtgraph
from PySide import QtCore, QtGui
from FrameQueue import FrameQueue
from PySimpleViewer.common.ProducerConsumerThread import ProducerConsumerThread
from PySimpleViewer.models.Config import Config
import time
import os
import threading

import Voxel

class DataFormat(object):
    DATA_2D = 0
    DATA_3D = 1

    COLOR_MAP_BW = 0
    COLOR_MAP_FULL = 1

    def __init__(self, name, title, dataType, elementType, colorMapType, levels,
                 numPoints, levels2 = None, isDepthType = False, scalingFactor = 1):
        self.name = name
        self.title = title
        self.dataType = dataType
        self.elementType = elementType
        self.colorMapType = colorMapType
        self.levels = levels
        self.numPoints = numPoints
        self.scalingFactor = 1
        self.isDepthType = isDepthType
        self.levels2 = levels2

        self.init()

    def init(self):
        if self.dataType == DataFormat.DATA_2D:
            if self.colorMapType == DataFormat.COLOR_MAP_BW:
                pos = np.array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1. ])\
                      *(self.levels[1] - self.levels[0])*self.scalingFactor \
                      + self.levels[0]*self.scalingFactor
                color = np.array(
                    [[0., 0., 0.],
                     [80.63808033, 80.63808033, 80.63808033],
                     [114.03946685, 114.03946685, 114.03946685],
                     [139.66925216, 139.66925216, 139.66925216],
                     [161.27616067, 161.27616067, 161.27616067],
                     [180.3122292, 180.3122292, 180.3122292],
                     [197.52215066, 197.52215066, 197.52215066],
                     [213.34830677, 213.34830677, 213.34830677],
                     [228.0789337, 228.0789337, 228.0789337],
                     [241.914241, 241.914241, 241.914241],
                     [255., 255., 255.]], dtype=np.uint16)
                self.cmap = pyqtgraph.ColorMap(pos, color)
                self.colorMap = self.cmap.getLookupTable(self.levels[0]*self.scalingFactor,
                                                         self.levels[1]*self.scalingFactor, self.numPoints,
                                                         alpha = True, mode='byte')
                # Used by HistogramLUTWidget only
                pos = np.array([0., 1.])
                self.cmap = pyqtgraph.ColorMap(pos, color)
            else:
                pos = np.array([0., 0.25, 0.50, 0.75, 1.])*(self.levels[1] - self.levels[0])\
                      *self.scalingFactor + self.levels[0]*self.scalingFactor
                color = np.array(
                    [[255, 0, 0, 255], [255, 255, 0, 255], [0, 255, 0, 255], [0, 255, 255, 255], [0, 0, 255, 255]],
                    dtype=np.uint16)
                self.cmap = pyqtgraph.ColorMap(pos, color)
                self.colorMap = self.cmap.getLookupTable(self.levels[0] * self.scalingFactor,
                                                         self.levels[1] * self.scalingFactor, self.numPoints,
                                                         alpha=True, mode='byte')
                # Used by HistogramLUTWidget only
                pos = np.array([0., 0.25, 0.50, 0.75, 1.])
                self.cmap = pyqtgraph.ColorMap(pos, color)
        else:
            if self.colorMapType == DataFormat.COLOR_MAP_BW:  # Uses sqrt(x) for B/W levels
                pos = np.array([0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]) \
                      * (self.levels[1] - self.levels[0]) * self.scalingFactor + self.levels[0] \
                                                                                 * self.scalingFactor
                color = np.array(
                    [[0., 0., 0.],
                     [0.31622777, 0.31622777, 0.31622777],
                     [0.4472136, 0.4472136, 0.4472136],
                     [0.54772256, 0.54772256, 0.54772256],
                     [0.63245553, 0.63245553, 0.63245553],
                     [0.70710678, 0.70710678, 0.70710678],
                     [0.77459667, 0.77459667, 0.77459667],
                     [0.83666003, 0.83666003, 0.83666003],
                     [0.89442719, 0.89442719, 0.89442719],
                     [0.9486833, 0.9486833, 0.9486833],
                     [1., 1., 1.]], dtype=np.float32)
                self.cmap = pyqtgraph.ColorMap(pos, color)
                self.colorMap = self.cmap.getLookupTable(0, 1, self.numPoints, alpha=True, mode='float')
            else:
                pos = np.array([0., 0.33, 0.67, 1.]) * (self.levels[1] - self.levels[0]) \
                      * self.scalingFactor + self.levels[0] * self.scalingFactor
                color = np.array([[0., 0., 0., 1.], [0., 0., 1., 1.0], [1., 0., 0., 1.0], [1., 1., 0., 1.0]],
                                 dtype=np.float32)
                self.cmap = pyqtgraph.ColorMap(pos, color)
                self.colorMap = self.cmap.getLookupTable(0, 1, self.numPoints, alpha=True, mode='float')

    def setScalingFactor(self, scalingFactor):
        self.scalingFactor = scalingFactor
        self.init()

    def setColorMapType(self, colorMapType):
        self.colorMapType = colorMapType
        self.init()

    def setLevels(self, levels):
        self.levels[0] = levels[0]
        self.levels[1] = levels[1]
        self.init()


class DataEngine(QtCore.QObject):

    statisticsChanged = QtCore.Signal(bool)
    rateFactorChanged = QtCore.Signal(float)

    dataFormats = {
        'phase': DataFormat('phase', 'Phase', DataFormat.DATA_2D, np.uint16, DataFormat.COLOR_MAP_FULL, [0, 4096],
                            4096),
        'phase_avg': DataFormat('phase_avg', 'Phase Average', DataFormat.DATA_2D, np.uint16, DataFormat.COLOR_MAP_FULL,
                                [0, 4096], 4096),
        'phase_std': DataFormat('phase_std', 'Phase Standard Deviation', DataFormat.DATA_2D, np.uint16,
                                DataFormat.COLOR_MAP_FULL, [0, 4096], 4096),
        'ambient': DataFormat('ambient', 'Ambient', DataFormat.DATA_2D, np.uint8, DataFormat.COLOR_MAP_FULL, [0, 16],
                              16),
        'amplitude': DataFormat('amplitude', 'Amplitude', DataFormat.DATA_2D, np.uint16, DataFormat.COLOR_MAP_BW,
                                [0, 1024], 1024),
        'amplitude_avg': DataFormat('amplitude_avg', 'Amplitude Average', DataFormat.DATA_2D, np.uint16,
                                    DataFormat.COLOR_MAP_BW, [0, 1024], 1024),
        'amplitude_std': DataFormat('amplitude_std', 'Amplitude Standard Deviation', DataFormat.DATA_2D, np.uint16,
                                    DataFormat.COLOR_MAP_BW, [0, 1024], 1024),
        'depth': DataFormat('depth', 'Depth (Z)', DataFormat.DATA_2D, np.float32, DataFormat.COLOR_MAP_FULL,
                            [0.0, 4096], 4096, isDepthType=True),
        'depth_avg': DataFormat('depth_avg', 'Depth Average (Z)', DataFormat.DATA_2D, np.float32,
                                DataFormat.COLOR_MAP_FULL, [0.0, 4096], 4096, isDepthType=True),
        'depth_std': DataFormat('depth_std', 'Depth Standard Deviation (Z)', DataFormat.DATA_2D, np.float32,
                                DataFormat.COLOR_MAP_FULL, [0.0, 4096], 4096, isDepthType=True),
        'distance': DataFormat('distance', 'Distance', DataFormat.DATA_2D, np.float32, DataFormat.COLOR_MAP_FULL,
                               [0.0, 4096], 4096, isDepthType=True),
        'distance_avg': DataFormat('distance_avg', 'Distance Average (meters)', DataFormat.DATA_2D, np.float32,
                                DataFormat.COLOR_MAP_FULL, [0.0, 4096], 4096, isDepthType=True),
        'distance_std': DataFormat('distance_std', 'Distance Standard Deviation (meters)', DataFormat.DATA_2D, np.float32,
                                   DataFormat.COLOR_MAP_FULL, [0.0, 4096], 4096, isDepthType=True),
        'flags': DataFormat('flags', 'Flags', DataFormat.DATA_2D, np.uint8, DataFormat.COLOR_MAP_FULL, [0, 16], 16),
        'pointcloud': DataFormat('pointcloud', 'Point Cloud', DataFormat.DATA_3D, np.float32, DataFormat.COLOR_MAP_BW,
                                 [0.0, 1024], 1024, levels2=[0, 4096], isDepthType=True),
    }

    dataAvailablePhase = QtCore.Signal(object, object, object)
    dataAvailablePhaseAverage = QtCore.Signal(object, object, object)
    dataAvailablePhaseStandardDeviation = QtCore.Signal(object, object, object)
    dataAvailableAmbient = QtCore.Signal(object, object, object)
    dataAvailableAmplitude = QtCore.Signal(object, object, object)
    dataAvailableAmplitudeAverage = QtCore.Signal(object, object, object)
    dataAvailableAmplitudeStandardDeviation = QtCore.Signal(object, object, object)
    dataAvailableDepth = QtCore.Signal(object, object, object)
    dataAvailableDepthAverage = QtCore.Signal(object, object, object)
    dataAvailableDepthStandardDeviation = QtCore.Signal(object, object, object)
    dataAvailableDistance = QtCore.Signal(object, object, object)
    dataAvailableDistanceAverage = QtCore.Signal(object, object, object)
    dataAvailableDistanceStandardDeviation = QtCore.Signal(object, object, object)
    dataAvailableFlags = QtCore.Signal(object, object, object)
    dataAvailablePointCloud = QtCore.Signal(object, object, object)

    def connectData(self, type, function, connectionType=QtCore.Qt.AutoConnection):
        if type == 'phase':
            self.dataAvailablePhase.connect(function, connectionType)
        elif type == 'phase_avg':
            self.dataAvailablePhaseAverage.connect(function, connectionType)
        elif type == 'phase_std':
            self.dataAvailablePhaseStandardDeviation.connect(function, connectionType)
        elif type == 'ambient':
            self.dataAvailableAmbient.connect(function, connectionType)
        elif type == 'amplitude':
            self.dataAvailableAmplitude.connect(function, connectionType)
        elif type == 'amplitude_avg':
            self.dataAvailableAmplitudeAverage.connect(function, connectionType)
        elif type == 'amplitude_std':
            self.dataAvailableAmplitudeStandardDeviation.connect(function, connectionType)
        elif type == 'depth':
            self.dataAvailableDepth.connect(function, connectionType)
        elif type == 'depth_avg':
            self.dataAvailableDepthAverage.connect(function, connectionType)
        elif type == 'depth_std':
            self.dataAvailableDepthStandardDeviation.connect(function, connectionType)
        elif type == 'distance':
            self.dataAvailableDistance.connect(function, connectionType)
        elif type == 'distance_avg':
            self.dataAvailableDistanceAverage.connect(function, connectionType)
        elif type == 'distance_std':
            self.dataAvailableDepthStandardDeviation.connect(function, connectionType)
        elif type == 'flags':
            self.dataAvailableFlags.connect(function, connectionType)
        elif type == 'pointcloud':
            self.dataAvailablePointCloud.connect(function, connectionType)
        else:
            print 'DataEngine: Could not connect data. Unknown type = ', type

    def disconnectData(self, type, function):
        if type == 'phase':
            self.dataAvailablePhase.disconnect(function)
        elif type == 'phase_avg':
            self.dataAvailablePhaseAverage.disconnect(function)
        elif type == 'phase_std':
            self.dataAvailablePhaseStandardDeviation.disconnect(function)
        elif type == 'ambient':
            self.dataAvailableAmbient.disconnect(function)
        elif type == 'amplitude':
            self.dataAvailableAmplitude.disconnect(function)
        elif type == 'amplitude_avg':
            self.dataAvailableAmplitudeAverage.disconnect(function)
        elif type == 'amplitude_std':
            self.dataAvailableAmplitudeStandardDeviation.disconnect(function)
        elif type == 'depth':
            self.dataAvailableDepth.disconnect(function)
        elif type == 'depth_avg':
            self.dataAvailableDepthAverage.disconnect(function)
        elif type == 'depth_std':
            self.dataAvailableDepthStandardDeviation.disconnect(function)
        elif type == 'distance':
            self.dataAvailableDistance.disconnect(function)
        elif type == 'distance_avg':
            self.dataAvailableDistanceAverage.disconnect(function)
        elif type == 'distance_std':
            self.dataAvailableDepthStandardDeviation.disconnect(function)
        elif type == 'flags':
            self.dataAvailableFlags.disconnect(function)
        elif type == 'pointcloud':
            self.dataAvailablePointCloud.disconnect(function)
        else:
            print 'DataEngine: Could not disconnect data. Unknown type = ', type

    def __init__(self, depthCameraController, queueLength = 3):
        super(DataEngine, self).__init__()

        self.isStatisticsEnabled = True

        self.frameRateEstimateCycles = 0
        self.rateFactor = 0.1
        self.data = {}
        self.frameSize = None
        self.frameID = 0
        self.frameTimestamp = 0
        self.depthCameraController = depthCameraController
        self.tofQueue = FrameQueue(queueLength)
        self.depthQueue = FrameQueue(queueLength)
        self.pointCloudQueue = FrameQueue(queueLength)

        self.depthCameraController.beforestart.connect(self.clearData, QtCore.Qt.DirectConnection)

        self.tofFrameThread = ProducerConsumerThread(producer=self.captureToFFrame, consumer=self.processToFFrame)
        self.depthFrameThread = ProducerConsumerThread(producer=self.captureDepthFrame, consumer=self.processDepthFrame)
        self.pointCloudFrameThread = ProducerConsumerThread(producer=self.capturePointCloudFrame,
                                                            consumer=self.processPointCloudFrame)

        self.depthCameraController.registerCallback(Voxel.DepthCamera.FRAME_RAW_FRAME_PROCESSED,
                                                    self.tofFrameThread.produceFunction)
        self.depthCameraController.registerCallback(Voxel.DepthCamera.FRAME_DEPTH_FRAME,
                                                    self.depthFrameThread.produceFunction)
        self.depthCameraController.registerCallback(Voxel.DepthCamera.FRAME_XYZI_POINT_CLOUD_FRAME,
                                                    self.pointCloudFrameThread.produceFunction)

        c = Config.getConfig(Config.VIEWER_MAIN_CONFIG)

        if c.hasOption('statistics', 'settling_time'):
            self.settlingTime = c.getFloat('statistics', 'settling_time')
        else:
            self.setSettlingTime(10)  # 10 seconds

    @QtCore.Slot(float)
    def setSettlingTime(self, settlingTime):
        self.settlingTime = settlingTime
        self.computeRateFactor()

        c = Config.getConfig(Config.VIEWER_MAIN_CONFIG)
        c.set('statistics', 'settling_time', self.settlingTime)

    def computeRateFactor(self):
        if self.frameRateEstimateCycles != 0:
            self.rateFactor = 1 - 10 ** (-12.0 / self.settlingTime / self.frameRate)
        else:
            self.rateFactor = 0.1  # Default value till better estimate of frame rate

        self.rateFactorChanged.emit(self.rateFactor)
        print('Using rate factor = ' + str(self.rateFactor) + '\n')
        ##Logger.writeLog(Voxel.LOG_INFO, 'Using rate factor = ' + str(self.rateFactor) + '\n')

    def enableStatistics(self):
        self.isStatisticsEnabled = True
        self.frameRateEstimateCycles = 0
        self.statisticsChanged.emit(self.isStatisticsEnabled)

    def disableStatistics(self):
        self.isStatisticsEnabled = False
        self.frameRateEstimateCycles = 0
        self.statisticsChanged.emit(self.isStatisticsEnabled)

    def getDataFormats(self):
        if self.isStatisticsEnabled:
            k = DataEngine.dataFormats.keys()
            k.sort()
            return k
        else:
            return ['amplitude', 'ambient', 'depth', 'distance', 'flags', 'phase', 'pointcloud']

    def getDepthCameraController(self):
        return self.depthCameraController

    def getFrameSize(self):
        return self.frameSize

    def clearData(self):
        self.frameRateEstimateCycles = 0
        self.tofQueue.clear()
        self.depthQueue.clear()
        self.pointCloudQueue.clear()

    def captureToFFrame(self, depthCamera, frame, type):
        if self.frameRateEstimateCycles == 0:
            self.currentTimestamp = frame.timestamp
            self.frameRate = 0
            self.computeRateFactor()
            self.frameRateEstimateCycles += 1
        elif self.frameRateEstimateCycles < 4:
            self.frameRate = (self.frameRate * (self.frameRateEstimateCycles - 1)
                              + 1.0 / ((frame.timestamp - self.currentTimestamp) * 1E-6)) / self.frameRateEstimateCycles
            self.frameRateEstimateCycles += 1
            self.currentTimestamp = frame.timestamp
            self.computeRateFactor()

        self.frameID = frame.id
        self.frameTimestamp = frame.timestamp
        self.tofQueue.put(frame)

        tofFrame = Voxel.ToF1608Frame.typeCast(frame)

        if not tofFrame:
            return

        size = tofFrame.size
        self.frameSize = [size.width, size.height]
        self.phaseArray = np.array(tofFrame._phase, copy=True)

    def processToFFrame(self):
        frame = self.tofQueue.get(timeout= 0.25)
        if frame is None:
            return False
        tofFrame = Voxel.ToF1608Frame.typeCast(frame)
        if not tofFrame:
            tofFrame = Voxel.ToF16IQFrame.typeCast(frame)
            if not tofFrame:
                self.tofQueue.release(frame)
                return False

            i = np.array(tofFrame._i)
            q = np.array(tofFrame._q)
            c = i + 1j*q

            a = np.abs(c)
            p = np.angle(c)

            p = ((p < 0)*(2*math.pi + p) + (p >= 0)*p)*(4096/(2*math.pi))
            amb = np.zeros(p.size)
            flags = np.zeros(p.size)
        else:
            a = np.array(tofFrame._amplitude)
            p = np.array(tofFrame._phase, copy=True)
            amb = np.array(tofFrame._ambient)
            flags = np.array(tofFrame._flags)

        size = tofFrame.size

        a1 = np.transpose(a.reshape((size.height, size.width)))
        self.data["amplitude"] = a1
        self.dataAvailableAmplitude.emit(frame.id, frame.timestamp, a1)

        p1 = np.transpose(p.reshape((size.height, size.width)))
        self.data["phase"] = p1
        self.dataAvailablePhase.emit(frame.id, frame.timestamp, p1)

        amb1 = np.transpose(amb.reshape(size.height, size.width))
        self.data["ambient"] = amb1
        self.dataAvailableAmbient.emit(frame.id, frame.timestamp, amb1)

        flags1 = np.transpose(flags.reshape((size.height, size.width)))
        self.data["flags"] = flags1
        self.dataAvailableFlags.emit(frame.id, frame.timestamp, flags1)

        s = DataEngine.dataFormats['phase'].levels[1]

        if self.isStatisticsEnabled:
            p2 = np.bitwise_and((p1 + 2048), 0xFFF)
            if not self.data.has_key('phase_avg') or not self.data['phase_avg'].shape == p1.shape:
                # self.phaseComplexAverage = self.rateFactor*np.exp(2j*math.pi*p1/s)
                # self.data["phase_avg"] = np.angle(self.phaseComplexAverage)
                # self.data["phase_std"] = np.sqrt(1 - np.abs(self.phaseComplexAverage))*(math.sqrt(2)*s)
                self.phaseAverage = self.rateFactor * p1
                self.phaseAverage2 = self.rateFactor * p2
                pa2 = self.phaseAverage2 - 2048
                pa2 += (pa2 < 0) * 4096
                phaseAverage = np.minimum(self.phaseAverage, pa2)
                self.data["phase_avg"] = phaseAverage
                self.phaseVariance = self.rateFactor * np.square(p1 - self.phaseAverage)
                self.phaseVariance2 = self.rateFactor * np.square(p2 - self.phaseAverage2)
                phaseStd = np.sqrt(np.minimum(self.phaseVariance, self.phaseVariance2))
                self.data["phase_std"] = phaseStd

                amplitudeAverage = self.rateFactor * a1
                self.amplitudeAverage = amplitudeAverage
                self.data["amplitude_avg"] = amplitudeAverage
                self.amplitudeVariance = self.rateFactor * np.square(a1 - self.amplitudeAverage)
                amplitudeStd = np.sqrt(self.amplitudeVariance)
                self.data["amplitude_std"] = amplitudeStd

                self.dataAvailablePhaseAverage.emit(frame.id, frame.timestamp, phaseAverage)
                self.dataAvailablePhaseStandardDeviation.emit(frame.id, frame.timestamp, phaseStd)
                self.dataAvailableAmplitudeAverage.emit(frame.id, frame.timestamp, amplitudeAverage)
                self.dataAvailableAmplitudeStandardDeviation.emit(frame.id, frame.timestamp, amplitudeStd)

            else:
                f = (1 - self.rateFactor)
                self.phaseAverage *= f
                self.phaseAverage += self.rateFactor * p1
                self.phaseAverage2 *= f
                self.phaseAverage2 += self.rateFactor * p2
                pa2 = self.phaseAverage2 - 2048
                pa2 += (pa2 < 0) * 4096
                phaseAverage = np.minimum(self.phaseAverage, pa2)
                self.data["phase_avg"] = phaseAverage
                self.phaseVariance *= f
                self.phaseVariance += self.rateFactor * np.square(p1 - self.phaseAverage)
                self.phaseVariance2 *= f
                self.phaseVariance2 += self.rateFactor * np.square(p2 - self.phaseAverage2)
                phaseStd = np.sqrt(np.minimum(self.phaseVariance, self.phaseVariance2))
                self.data["phase_std"] = phaseStd

                # self.phaseComplexAverage *= f
                # self.phaseComplexAverage += self.rateFactor*np.exp(2j*math.pi*p1/s)
                # self.data["phase_avg"] = (np.angle(self.phaseComplexAverage) + math.pi)*s/(2*math.pi)
                # self.data["phase_std"] = np.sqrt(1 - np.abs(self.phaseComplexAverage))*(math.sqrt(2)*s)

                self.amplitudeAverage *= f
                self.amplitudeAverage += self.rateFactor * a1
                amplitudeAverage = np.copy(self.amplitudeAverage)
                self.data["amplitude_avg"] = amplitudeAverage
                self.amplitudeVariance *= f
                self.amplitudeVariance += self.rateFactor * np.square(a1 - self.amplitudeAverage)
                amplitudeStd = np.sqrt(self.amplitudeVariance)
                self.data["amplitude_std"] = amplitudeStd

                self.dataAvailablePhaseAverage.emit(frame.id, frame.timestamp, phaseAverage)
                self.dataAvailablePhaseStandardDeviation.emit(frame.id, frame.timestamp, phaseStd)
                self.dataAvailableAmplitudeAverage.emit(frame.id, frame.timestamp, amplitudeAverage)
                self.dataAvailableAmplitudeStandardDeviation.emit(frame.id, frame.timestamp, amplitudeStd)

            self.tofQueue.release(frame)

    def captureDepthFrame(self, depthCamera, frame, type):
        self.depthQueue.put(frame)

    def processDepthFrame(self):
        frame = self.depthQueue.get(timeout=0.25)
        if frame is None:
            return False

        depthFrame = Voxel.DepthFrame.typeCast(frame)
        if not depthFrame:
            self.depthQueue.release(frame)
            return

        d = np.array(depthFrame.depth)
        d1 = np.transpose(d.reshape(depthFrame.size.height, depthFrame.size.width))
        self.data["distance"] = d1
        self.dataAvailableDistance.emit(frame.id, frame.timestamp, d1)

        if self.isStatisticsEnabled:
            if not self.data.has_key('distance_avg') or not self.data['distance_avg'].shape == d1.shape:
                distanceAverage = self.rateFactor * d1
                self.distanceAverage = distanceAverage
                self.data["distance_avg"] = distanceAverage
                self.distanceVariance = self.rateFactor * np.square(d1 - self.distanceAverage)
                distanceStd = np.sqrt(self.distanceVariance)
                self.data["distance_std"] = distanceStd

                self.dataAvailableDistanceAverage.emit(frame.id, frame.timestamp, distanceAverage)
                self.dataAvailableDistanceStandardDeviation.emit(frame.id, frame.timestamp, distanceStd)
            else:
                f = (1 - self.rateFactor)
                self.distanceAverage *= f
                self.distanceAverage += self.rateFactor * d1
                distanceAverage = np.copy(self.distanceAverage)
                self.data["distance_avg"] = distanceAverage
                self.distanceVariance *= f
                self.distanceVariance += self.rateFactor * np.square(d1 - self.distanceAverage)
                distanceStd = np.sqrt(self.distanceVariance)
                self.data["distance_std"] = distanceStd

                self.dataAvailableDistanceAverage.emit(frame.id, frame.timestamp, distanceAverage)
                self.dataAvailableDistanceStandardDeviation.emit(frame.id, frame.timestamp, distanceStd)

        self.depthQueue.release(frame)

    def capturePointCloudFrame(self, depthCamera, frame, type):
        self.pointCloudQueue.put(frame)

    def processPointCloudFrame(self):
        frame = self.pointCloudQueue.get(timeout=0.25)
        if frame is None:
            return False

        pointCloudFrame = Voxel.XYZIPointCloudFrame.typeCast(frame)
        if not pointCloudFrame:
            self.pointCloudQueue.release(frame)
            return False

        pcf = np.array(pointCloudFrame, copy=True)
        if hasattr(self, 'phaseArray') and pcf[:,0].shape == self.phaseArray.shape:
            # Remove invalid pixels
            mask = (self.phaseArray < 4095) & (self.phaseArray > 0)

            pcf[:, 0] *= mask
            pcf[:, 1] *= mask
            pcf[:, 2] *= mask

        self.data["pointcloud"] = pcf
        self.dataAvailablePointCloud.emit(frame.id, frame.timestamp, pcf)

        d = self.data['pointcloud'][:, 2]
        d1 = np.transpose(d.reshape((self.frameSize[1], self.frameSize[0])))
        self.data["depth"] = d1
        self.dataAvailableDepth.emit(frame.id, frame.timestamp, d1)

        if self.isStatisticsEnabled:
            if not self.data.has_key('depth_avg') or not self.data['depth_avg'].shape == d1.shape:
                depthAverage = self.rateFactor * d1
                self.depthAverage = depthAverage
                self.data["depth_avg"] = self.depthAverage
                self.depthVariance = self.rateFactor * np.square(d1 - self.depthAverage)
                depthStd = np.sqrt(self.depthVariance)
                self.data["depth_std"] = depthStd

                self.dataAvailableDepthAverage.emit(frame.id, frame.timestamp, depthAverage)
                self.dataAvailableDepthStandardDeviation.emit(frame.id, frame.timestamp, depthStd)
            else:
                f = (1 - self.rateFactor)
                self.depthAverage *= f
                self.depthAverage += self.rateFactor * d1
                depthAverage = self.depthAverage
                self.data["depth_avg"] = self.depthAverage
                self.depthVariance *= f
                self.depthVariance += self.rateFactor * np.square(d1 - self.depthAverage)
                depthStd = np.sqrt(self.depthVariance)
                self.data["depth_std"] = depthStd

                self.dataAvailableDepthAverage.emit(frame.id, frame.timestamp, depthAverage)
                self.dataAvailableDepthStandardDeviation.emit(frame.id, frame.timestamp, depthStd)

        self.pointCloudQueue.release(frame)

    def stop(self):
        self.tofFrameThread.stop()
        self.depthFrameThread.stop()
        self.pointCloudFrameThread.stop()



        



