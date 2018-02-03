#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

import Voxel
import time
import threading
import os
from socket import *
import struct
from PySide import QtCore

class StreamSource(QtCore.QObject):
    paused = QtCore.Signal()
    resumed = QtCore.Signal()
    stopped = QtCore.Signal()
    beforestart = QtCore.Signal()
    started = QtCore.Signal()

    def __init__(self, name, parent=None):
        super(StreamSource, self).__init__(parent)
        self.callback = None
        self.name = name
        self.pos = 0
        self.timestamp = 0
        self.paus = False

        self.frameStreamHandler = None

    def isInitialized(self):
        pass

    def getName(self):
        return self.name

    def setCallback(self, callback):
        self.callback = callback

    def removeCallback(self):
        self.callback = None

    def start(self):
        return False

    def pause(self):
        if self.isRunning():
            self.paus = True
            self.paused.emit()
            return True
        else:
            return False

    def resume(self):
        if self.isRunning():
            if self.isPaused():
                self.paus = False
                self.resumed.emit()
                return True
            else:
                return False
        else:
            self.paus = False
            return False

    def stop(self):
        return False

    def isRunning(self):
        return False

    def isPaused(self):
        return self.paus

    def isSeekable(self):
        return False

    def isLiveStream(self):
        return False

    def length(self):
        return 0

    def currentPosition(self):
        return self.pos

    def currentTimestamp(self):
        return self.timestamp

    def seek(self, pos):
        return False

    def getROI(self):
        return None

    def getBinning(self):
        return None

    def getStreamParamf(self, name):
        if self.frameStreamHandler is not None:
            r, f = self.frameStreamHandler.getStreamParamf(name)
            if r:
                return f
            else:
                return 0
        else:
            return 0

    def getDepthScalingFactor(self):
        return self.getStreamParamf("depthScalingFactor")

    def getAmplitudeScalingFactor(self):
        return self.getStreamParamf("amplitudeScalingFactor")


class DepthCameraStreamSource(StreamSource):
    def __init__(self, depthCamera):
        super(DepthCameraStreamSource, self).__init__("Live Capture")
        self.setDepthCamera(depthCamera)

    def isInitialized(self):
        return not (self.depthCamera is None)

    def setDepthCamera(self, depthCamera):
        self.depthCamera = depthCamera
        self.frameStreamHandler = depthCamera

        if self.depthCamera:
            self.depthCamera.clearAllCallbacks()
            self.depthCamera.registerCallback(Voxel.DepthCamera.FRAME_RAW_FRAME_UNPROCESSED, self.callbackInternal)
            self.depthCamera.registerCallback(Voxel.DepthCamera.FRAME_RAW_FRAME_PROCESSED, self.callbackInternal)
            self.depthCamera.registerCallback(Voxel.DepthCamera.FRAME_DEPTH_FRAME, self.callbackInternal)
            self.depthCamera.registerCallback(Voxel.DepthCamera.FRAME_XYZI_POINT_CLOUD_FRAME, self.callbackInternal)

    def start(self):
        if self.isPaused():
            return self.resume()

        if self.depthCamera and not self.depthCamera.isRunning():
            self.beforestart.emit()
            if not self.depthCamera.start():
                return False
            self.started.emit()
            return True
        else:
            return False

    def isPaused(self):
        if self.depthCamera:
            return self.depthCamera.isPaused()
        else:
            return False

    def pause(self):
        if self.depthCamera:
            if self.depthCamera.pause():
                self.paused.emit()
                return True
            else:
                return False
        else:
            return False

    def resume(self):
        if self.depthCamera:
            if self.depthCamera.resume():
                self.resumed.emit()
                return True
            else:
                return False
        else:
            return False

    def stop(self):

        if self.isPaused():
            self.resume()

        if self.depthCamera:
            if self.depthCamera.isRunning():
                if not self.depthCamera.stop():
                    return False
                self.stopped.emit()
                return True
            else:
                self.stopped.emit()
                return True
        else:
            return False

    def isLiveStream(self):
        return True

    def isRunning(self):
        if self.depthCamera:
            return self.depthCamera.isRunning()
        else:
            return False

    def callbackInternal(self, depthCamera, frame, type):
        self.pos = frame.id
        self.timestamp = frame.timestamp

        if self.isPaused():
            return

        if self.callback:
            self.callback(depthCamera, frame, type)

    def __del__(self):
        if self.isRunning():
            self.stop()

        del self.depthCamera


class FileStreamSource(StreamSource):
    def __init__(self, filename, cameraSystem):
        super(FileStreamSource, self).__init__(os.path.basename(filename))
        self.filename = filename
        self.runThread = None
        self.running = False
        self.cameraSystem = cameraSystem

        self.frameStream = Voxel.FrameStreamReader(str(filename), cameraSystem)
        self.frameStreamHandler = self.frameStream

    def isInitialized(self):
        return self.frameStream.isStreamGood()

    def isLiveStream(self):
        return False

    def isRunning(self):
        return self.running

    def isSeekable(self):
        return True

    def currentPosition(self):
        return self.frameStream.currentPosition()

    def currentTimestamp(self):
        if self.timestamp:
            return self.timestamp
        else:
            return 0

    def length(self):
        return self.frameStream.size()

    def seek(self, pos):
        self.frameStream.seekTo(pos)

        if not self.isRunning():
            self.processNext()

    def processNext(self):
        if not self.frameStream.readNext():
            return False

        self.timestamp = self.frameStream.frames[Voxel.DepthCamera.FRAME_RAW_FRAME_UNPROCESSED].timestamp
        self.frameID = self.frameStream.frames[Voxel.DepthCamera.FRAME_RAW_FRAME_UNPROCESSED].id

        if self.callback:
            self.callback(None, self.frameStream.frames[Voxel.DepthCamera.FRAME_RAW_FRAME_UNPROCESSED],
                          Voxel.DepthCamera.FRAME_RAW_FRAME_UNPROCESSED)
            self.callback(None, self.frameStream.frames[Voxel.DepthCamera.FRAME_RAW_FRAME_PROCESSED],
                          Voxel.DepthCamera.FRAME_RAW_FRAME_PROCESSED)
            self.callback(None, self.frameStream.frames[Voxel.DepthCamera.FRAME_DEPTH_FRAME],
                          Voxel.DepthCamera.FRAME_DEPTH_FRAME)
            self.callback(None, self.frameStream.frames[Voxel.DepthCamera.FRAME_XYZI_POINT_CLOUD_FRAME],
                          Voxel.DepthCamera.FRAME_XYZI_POINT_CLOUD_FRAME)

        if self.isPaused() or not self.isRunning():
            self.frameStream.seekTo(self.frameStream.currentPosition() - 1)

        return True

    def runLoop(self):
        lastTimeStamp = -1
        lastFrameIndex = -1
        while self.running:
            t = time.time()
            if not self.processNext():
                self.running = False
                self.stopped.emit()

            t2 = (time.time() - t) * 1E6
            if lastTimeStamp > 0:
                t = (self.timestamp - lastTimeStamp - t2) * 1E-6

                if lastFrameIndex > 0 and self.frameID > lastFrameIndex:
                    t /= (self.frameID - lastFrameIndex)

                if t > 0:
                    time.sleep(t)

            if not self.isPaused():
                lastTimeStamp = self.timestamp
                lastFrameIndex = self.frameID

    def start(self):
        if not self.frameStream.isStreamGood():
            return False

        if self.isPaused():
            self.resume()

        if self.currentPosition() >= self.length() - 1:
            self.seek(0)
        self.beforestart.emit()
        self.running = True
        self.runThread = threading.Thread(target=self.runLoop)
        self.runThread.start()
        self.started.emit()
        return True

    def pause(self):
        if not super(FileStreamSource, self).pause():
            return False

        if self.isRunning() and self.runThread is not None and self.runThread.is_alive():
            self.running = False
            self.runThread.join()

        self.running = False
        self.runThread = None
        return True

    def stop(self):
        if not self.isPaused():
            if not self.pause():
                return False

        self.resume()
        self.stopped.emit()
        self.seek(0)
        return True

    def __del__(self):
        self.stop()

class DepthCameraStreamController(QtCore.QObject):
    started = QtCore.Signal()
    beforestart = QtCore.Signal()
    stopped = QtCore.Signal()
    paused = QtCore.Signal()
    resumed = QtCore.Signal()
    sourceListChanged = QtCore.Signal()
    sourceSelected = QtCore.Signal(int)
    onDepthCameraSet = QtCore.Signal()

    def __init__(self, cameraSystem, depthCamera=None):
        super(DepthCameraStreamController, self).__init__()
        self.depthCamera = depthCamera
        self.cameraSystem = cameraSystem
        self.depthCameraSourceIndex = -1

        self.callbacks = []
        self.sources = []

        for i in range(0, Voxel.DepthCamera.FRAME_TYPE_COUNT):
            self.callbacks.append([])

        if self.depthCamera is not None:
            self.addDepthCameraSource()

    def addDepthCameraSource(self):
        self.sources.append(DepthCameraStreamSource(self.depthCamera))
        self.depthCameraSourceIndex = len(self.sources) - 1
        self.sourceListChanged.emit()
        self.setCurrentSource(self.depthCameraSourceIndex)

    def getCameraSystem(self):
        return self.cameraSystem

    def addDepthCameraSource(self):
        self.sources.append(DepthCameraStreamSource(self.depthCamera))
        self.depthCameraSourceIndex = len(self.sources) - 1
        self.sourceListChanged.emit()
        self.setCurrentSource(self.depthCameraSourceIndex)

    def getCameraSystem(self):
        return self.cameraSystem

    def disconnectDepthCamera(self, onlyFromUI=False):
        if not self.depthCamera:
            return

        self.stop()

        if not onlyFromUI:
            if not self.cameraSystem.disconnect(self.depthCamera):
                Logger.writeLog(Voxel.LOG_ERROR, 'Failed to disconnect depth camera')

        del self.depthCamera
        self.depthCamera = None

        if self.currentSource == self.sources[self.depthCameraSourceIndex]:
            self.currentSource = None

        del self.sources[self.depthCameraSourceIndex]
        self.depthCameraSourceIndex = -1
        self.sourceListChanged.emit()

    def resetDepthCamera(self):
        if not self.depthCamera:
            return

        self.stop()

        if not self.cameraSystem.disconnect(self.depthCamera, True):
            '''Logger.writeLog(Voxel.LOG_ERROR, 'Failed to reset depth camera')'''

        del self.depthCamera
        self.depthCamera = None

        if self.currentSource == self.sources[self.depthCameraSourceIndex]:
            self.currentSource = None

        del self.sources[self.depthCameraSourceIndex]
        self.depthCameraSourceIndex = -1
        self.sourceListChanged.emit()

    def setDepthCamera(self, depthCamera):
        self.depthCamera = depthCamera

        self.onDepthCameraSet.emit()

        if self.depthCameraSourceIndex >= 0:
            r = self.currentSource.isRunning()
            if self.currentSource == self.sources[self.depthCameraSourceIndex] and r:
                self.currentSource.stop()

            self.sources[self.depthCameraSourceIndex].setDepthCamera(depthCamera)

            if self.currentSource == self.sources[self.depthCameraSourceIndex] and r:
                self.currentSource.start()
        else:
            self.addDepthCameraSource()
            self.sources[self.depthCameraSourceIndex].setDepthCamera(depthCamera)

        self.sourceSelected.emit(self.currentSourceIndex)

    def getDepthCamera(self):
        return self.depthCamera

    def getCurrentSource(self):
        if hasattr(self, 'currentSource'):
            return self.currentSource
        else:
            return None

    def setCurrentSource(self, pos):
        if pos >= len(self.sources):
            print "DepthCameraStreamController: Invalid source ID = ", pos, ", Valid = [0, ", (len(self.sources) - 1)
            return False

        if hasattr(self, 'currentSource') and self.currentSource is not None:
            self.currentSource.stop()
            self.currentSource.removeCallback()
            self.currentSource.started.disconnect(self.started)
            self.currentSource.beforestart.disconnect(self.beforestart)
            self.currentSource.stopped.disconnect(self.stopped)
            self.currentSource.paused.disconnect(self.paused)
            self.currentSource.resumed.disconnect(self.resumed)

        self.currentSource = self.sources[pos]
        self.currentSourceIndex = pos
        self.currentSource.setCallback(self.callbackInternal)
        self.currentSource.started.connect(self.started)
        self.currentSource.beforestart.connect(self.beforestart)
        self.currentSource.stopped.connect(self.stopped)
        self.currentSource.paused.connect(self.paused)
        self.currentSource.resumed.connect(self.resumed)
        self.sourceSelected.emit(pos)
        return True

    def registerCallback(self, type, callback):
        self.callbacks[type].append(callback)
        return True

    def clearCallback(self, type, callback):
        for i in self.callbacks[type]:
            if i == callback:
                self.callbacks[type].remove(i)
                return True
        return False

    def getSources(self):
        return self.sources

    def getCurrentSource(self):
        if hasattr(self, 'currentSource'):
            return self.currentSource
        else:
            return None

    def addFileStreamSource(self, filename):
        i = 0
        for s in self.sources:
            if isinstance(s, FileStreamSource):
                if s.filename == filename:
                    return i
            i = i + 1

        self.sources.append(FileStreamSource(filename, self.cameraSystem))
        self.sourceListChanged.emit()
        return i

    def removeStreamSource(self, index):
        if index < 0 or index >= len(self.sources):
            return False

        if isinstance(self.sources[index], DepthCameraStreamSource):
            self.disconnectDepthCamera(onlyFromUI=True)

        del self.sources[index]
        self.sourceListChanged.emit()
        return True

    def isRunning(self):
        if hasattr(self, 'currentSource') and self.currentSource is not None:
            return self.currentSource.isRunning()
        else:
            return False

    def isPaused(self):
        if hasattr(self, 'currentSource') and self.currentSource is not None:
            return self.currentSource.isPaused()
        else:
            return False

    def callbackInternal(self, depthCamera, frame, type):
        for f in self.callbacks[type]:
            f(depthCamera, frame, type)

    def start(self):
        if hasattr(self, 'currentSource') and self.currentSource is not None:
            return self.currentSource.start()
        else:
            return False

    def pause(self):
        if hasattr(self, 'currentSource') and self.currentSource is not None:
            return self.currentSource.pause()
        else:
            return False

    def stop(self):
        if hasattr(self, 'currentSource') and self.currentSource is not None:
            return self.currentSource.stop()
        else:
            return False


