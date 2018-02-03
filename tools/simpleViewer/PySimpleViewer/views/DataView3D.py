#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#
from PySide import QtGui, QtCore
import pyqtgraph.opengl as gl
import pyqtgraph
import Voxel

import numpy as np

import math

import time

import copy

from DataView import DataView

from QxtSpanSlider import QxtSpanSlider

class DataView3DMenu(QtGui.QMenu):
  
  def __init__(self, parent):
    super(DataView3DMenu, self).__init__(parent)
    
    self.resetAction = QtGui.QAction(QtGui.QIcon.fromTheme('reset'), '&Reset view', parent)
    self.resetAction.setShortcut('R')
    self.resetAction.triggered.connect(parent.resetCamera)
    self.addAction(self.resetAction)
    
    actions = {'X': parent.viewX, 'Y': parent.viewY, 'Z': parent.viewZ}
    for x in ['X', 'Y', 'Z']:
      a = QtGui.QAction(QtGui.QIcon().fromTheme('view'), 'View ' + x, parent)
      a.triggered.connect(actions[x])
      a.setShortcut(x)
      self.addAction(a)
      
    self.addSeparator()
    
    self.exportAction = QtGui.QAction(QtGui.QIcon().fromTheme('export'), '&Export As Point Cloud Data (PCD)', parent)
    self.exportAction.setShortcut('E')
    self.exportAction.triggered.connect(parent.exportImage)
    self.addAction(self.exportAction)


class MyGLViewWidget(gl.GLViewWidget):
  """ Override GLViewWidget with enhanced behavior and Atom integration.
  
  """
  #: Fired in update() method to synchronize listeners.
  sigUpdate = QtCore.Signal()
  
  export = QtCore.Signal()
  
  def __init__(self, parent = None):
    gl.GLViewWidget.__init__(self, parent)
    
    self.defaults = {
        'center': QtGui.QVector3D(0, 0, 0),  ## will always appear at the center of the widget
        'distance': 1,         ## distance of camera from center
        'fov':  60,               ## horizontal field of view in degrees
        'elevation':  -90,         ## camera's angle of elevation in degrees
        'azimuth': -90,            ## camera's azimuthal angle in degrees 
        'rotation': 0
                                  ## (rotation around z-axis 0 points along x-axis)
    }
    
    self.dataView3D = parent
    
    self.menu = DataView3DMenu(self)
    self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
    
  def contextMenuEvent(self, e):
    self.menu.popup(e.globalPos())
    
  def resetCamera(self):
    self.opts['center'] = copy.deepcopy(self.defaults['center'])
    self.opts['distance'] = copy.deepcopy(self.defaults['distance'])
    self.opts['fov'] = copy.deepcopy(self.defaults['fov'])
    self.opts['elevation'] = copy.deepcopy(self.defaults['elevation'])
    self.opts['azimuth'] = copy.deepcopy(self.defaults['azimuth'])
    self.opts['rotation'] = copy.deepcopy(self.defaults['rotation'])
    self.update()
    
  def viewMatrix(self):
    tr = QtGui.QMatrix4x4()
    center = self.opts['center']
    tr.translate(0.0, 0.0, -self.opts['distance'])
    tr.rotate(self.opts['elevation']-90, 1, 0, 0)
    tr.rotate(self.opts['azimuth']+90, 0, 0, -1)
    tr.rotate(self.opts['rotation'], 0, 1, 0)
    tr.translate(-center.x(), -center.y(), -center.z())
    return tr
  
  def viewZ(self):
    self.opts['rotation'] = 0
    self.opts['elevation'] = -90
    self.update()
    
  def viewY(self):
    self.opts['rotation'] = 90
    self.opts['elevation'] = -90
    self.update()
    
  def viewX(self):
    self.opts['rotation'] = 0
    self.opts['elevation'] = 0
    self.update()
    
  def exportImage(self):
    self.dataView3D.exportImage()
  
  def orbitAbout(self, rotation, elevation):
    self.opts['rotation'] += rotation
    self.opts['elevation'] += elevation
    self.update()
  
  #def mouseMoveEvent(self, ev):
    #diff = ev.pos() - self.mousePos
    #self.mousePos = ev.pos()
    
    #if ev.buttons() == QtCore.Qt.LeftButton:
      #self.orbitAbout(diff.x(), diff.y())
    #else:
      #super(MyGLViewWidget, self).mouseMoveEvent(ev)
      
  def evalKeyState(self):
    speed = 2.0
    if len(self.keysPressed) > 0:
      for key in self.keysPressed:
        if key == QtCore.Qt.Key_Right:
          self.orbitAbout(rotation=-speed, elevation=0)
        elif key == QtCore.Qt.Key_Left:
          self.orbitAbout(rotation=speed, elevation=0)
        elif key == QtCore.Qt.Key_Up:
          self.orbitAbout(rotation=0, elevation=-speed)
        elif key == QtCore.Qt.Key_Down:
          self.orbitAbout(rotation=0, elevation=speed)
        elif key == QtCore.Qt.Key_PageUp:
          pass
        elif key == QtCore.Qt.Key_PageDown:
          pass
        self.keyTimer.start(16)
    else:
      self.keyTimer.stop()
  
  def mouseMoveEvent(self, ev):
    diff = ev.pos() - self.mousePos
    self.mousePos = ev.pos()
        
    if ev.buttons() == QtCore.Qt.LeftButton:
      self.orbitAbout(-diff.x(), diff.y())
    else:
      super(MyGLViewWidget, self).mouseMoveEvent(ev)
      
  def setCenter(self, center):
    self.opts['center'] = QtGui.QVector3D(center[0], center[1], center[2])
    self.update()

  def keyPressEvent(self, ev):
    if ev.key() == QtCore.Qt.Key_R:
      self.resetCamera()
    elif ev.key() == QtCore.Qt.Key_X:
      self.viewX()
    elif ev.key() == QtCore.Qt.Key_Y:
      self.viewY()
    elif ev.key() == QtCore.Qt.Key_Z:
      self.viewZ()
    elif ev.key() == QtCore.Qt.Key_E:
      self.export.emit()
    else:
      if ev.modifiers() & QtCore.Qt.ControlModifier:
        ev.ignore()
      else:
        super(MyGLViewWidget, self).keyPressEvent(ev)

class DataView3D(DataView):
  
  dataAvailable = QtCore.Signal()
  
  def __init__(self, dataEngine, dataFormat, parent = None):
    DataView.__init__(self, dataEngine, dataFormat, parent)
    
    self.updateCount = 0
    
    self.setMinimumHeight(200)
    self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    
    l = QtGui.QVBoxLayout(self)
    
    self.glWidget = MyGLViewWidget(self)
    
    l.addWidget(self.glWidget)
    
    hlayout = QtGui.QHBoxLayout()
    hlayout.addWidget(QtGui.QLabel('Depth Threshold:'))
    
    self.spanSlider = QxtSpanSlider()
    self.spanSlider.floatLowerPositionChanged.connect(self.updateLowerLevel)
    self.spanSlider.floatUpperPositionChanged.connect(self.updateUpperLevel)
    hlayout.addWidget(self.spanSlider)
    
    l.addLayout(hlayout)
    
    self.glWidget.opts['distance'] = 20
    
    self.gridItem = gl.GLGridItem(size = QtGui.QVector3D(10,10,1))
    self.glWidget.addItem(self.gridItem)
    
    self.axisItem = gl.GLAxisItem()
    self.axisItem.setSize(3,3,3)
    self.glWidget.addItem(self.axisItem)
    
    pos = np.array([[0., 0., 0.]])
    color = np.array([[0., 0., 0., 0.]])
    
    self.scatterItem = gl.GLScatterPlotItem(pxMode = True, size = 2, pos = pos, color = color)
    self.glWidget.addItem(self.scatterItem)
    
    self.glWidget.resetCamera()
    
    self.glWidget.export.connect(self.exportImage)
    
    DataView.communicator.setCurrentPoint2D.connect(self.setCenter, QtCore.Qt.QueuedConnection)
    
    DataView.communicator.thresholdsChanged.connect(self.setThresholds, QtCore.Qt.QueuedConnection)
    
    self.currentPCF = None
    
    self.dataEngine.getDepthCameraController().started.connect(self.streamStarted)
    
    self.setSpanKeyModifier(QtCore.Qt.ControlModifier)

  @QtCore.Slot()
  def streamStarted(self):
    self.updateCount = 0
    
  @QtCore.Slot()
  def resetView(self):
    self.glWidget.resetCamera()
    
    self.updateDataFormat()
    
  @QtCore.Slot()
  def exportImage(self):
    if self.currentPCF is None:
      QtGui.QMessageBox.critical(self, 'Blank Image', 'There is no point cloud to export.')
      return
    
    filename, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save PCD Snapshot', filter = "Point Cloud Data files (*.pcd)")
    
    if filename:
      try:
        with open(filename, 'w') as f:
          f.write('# .PCD v.7 - Point Cloud Data file format\n' +
            'VERSION .7\n' +
            'FIELDS x y z i\n' +
            'SIZE 4 4 4 4\n' +
            'TYPE F F F F\n' +
            'COUNT 1 1 1 1\n' +
            'WIDTH %d\n'%self.currentPCF.shape[0] +
            'HEIGHT 1\n' + 
            'VIEWPOINT 0 0 0 1 0 0 0\n' +
            'POINTS %d\n'%self.currentPCF.shape[0] +
            'DATA ascii\n')
          
          np.savetxt(f, self.currentPCF, delimiter=' ')
      except Exception, e:
        QtGui.QMessageBox.critical(self, 'Save PCD Failed', 'Failed to save PCD to "' + filename + '".')
        return
      
  
  @QtCore.Slot()
  def updateDataFormat(self):
    if self.dataFormat is None:
      return
    
    s = self.dataEngine.depthCameraController.getCurrentSource()
    
    if s is not None:
      d = s.getDepthScalingFactor()
      a = s.getAmplitudeScalingFactor()
      
      self.depthScalingFactor = d
      self.dataFormat.setScalingFactor(a)
      self.depthLevels = [self.dataFormat.levels2[0]*d, self.dataFormat.levels2[1]*d]
      self.spanSlider.setFloatRange(self.depthLevels[0], self.depthLevels[1], d)
    
  @QtCore.Slot(object)
  def setCenter(self, point):
    
    if self.currentPCF is None:
      return
    
    frameSize = self.dataEngine.frameSize
    
    if not frameSize:
      return
    
    x = int(point.x())
    y = int(point.y())
    
    if x < 0 or x > frameSize[0] or y < 0 or y > frameSize[1]:
      return
    
    rowOrderValue = frameSize[0]*y + x
    
    try:
      p = self.currentPCF[rowOrderValue, 0:3]
      self.glWidget.setCenter(p)
    except Exception, e:
      pass
        
  @QtCore.Slot()
  def displayData(self):
    pcf = self.dataQueue.tryGet()
    
    self.updateCount = self.updateCount + 1
    
    self.currentPCF = pcf

    if pcf is None:
      return
    
    self.pos = pcf[:,0:3]
    self.color = (pcf[:,3:4].reshape((self.pos.shape[0],)))
    
    #self.color = np.linspace(0, 1, pos.shape[0])
    
    # Uncomment these lines to use dynamic LUT
    #mc = np.amax(self.color)
    #if mc > 0:
    #  self.color = self.color/mc*256
    self.color = (self.color*self.dataFormat.numPoints).astype(int)
    
    if self.updateCount == 1:
      self.resetView()
    
    self.clipAndShow()
    
    
  @QtCore.Slot(str, object, object)
  def setThresholds(self, name, lower, upper):
    if name == 'amplitude' or name == 'amplitude_avg' or name == 'amplitude_std':
      self.dataFormat.setLevels([lower, upper])
      
      try:
        self.clipAndShow()
      except Exception, e:
        pass
    elif name == 'depth' or name == 'depth_avg' or name == 'depth_std':
      s = self.dataEngine.depthCameraController.getCurrentSource()
    
      if s is not None:
        d = s.getDepthScalingFactor()
        if d > 1E-12:
          self.spanSlider.setFloatRange(lower, upper, d)
  
  def clipAndShow(self):
    if not hasattr(self, 'pos') or not hasattr(self, 'color') or self.pos is None or self.color is None:
      return
    
    posClip = (self.pos[:,2] <= self.depthLevels[1]) & (self.pos[:,2] >= self.depthLevels[0])
    
    pos = np.array(self.pos, copy = True)
    pos[:,0] *= posClip
    pos[:,1] *= posClip
    pos[:,2] *= posClip
    color =  np.take(self.dataFormat.colorMap, self.color, axis = 0, mode = 'clip')
    self.scatterItem.setData(pos = pos, color = color)
    
  @QtCore.Slot(int)
  def updateLowerLevel(self, lower):
    self.depthLevels[0] = lower
    self.clipAndShow()
    
  @QtCore.Slot(int)
  def updateUpperLevel(self, upper):
    self.depthLevels[1] = upper
    self.clipAndShow()
