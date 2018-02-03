#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtGui, QtCore
import pyqtgraph

import Voxel
import numpy as np

import time

from PySimpleViewer.models.DataQueue import DataQueue

from PySimpleViewer.models.DataEngine import *

class DataViewCommunicator(QtCore.QObject):
  
  setCurrentPoint2D = QtCore.Signal(object)
  
  setShiftClickPoint2D = QtCore.Signal(object)
  
  viewRangeChanged = QtCore.Signal(object, object, object, object) # x1, y1, x2, y2
  
  thresholdsChanged = QtCore.Signal(str, object, object)
  
  def __init__(self, parent = None):
    super(DataViewCommunicator, self).__init__(parent)

class DataView(QtGui.QWidget):
  
  dataEnqueued = QtCore.Signal()
  
  communicator = DataViewCommunicator() # Static object for communication from and to DataView instances
  
  LinkedViewBoxes = {}
  
  def __init__(self, dataEngine, dataFormat, parent = None):
    super(DataView, self).__init__(parent)
    
    self.dataFormat = None
    self.dataEngine = dataEngine
    
    self.dataQueue = DataQueue()
    
    DataView.setDataFormat(self, dataFormat)
    
    self.dataEnqueued.connect(self.displayData, QtCore.Qt.QueuedConnection)
    
    self.spanKeyModifier = None
    
    self.statusBar = None
    
  @QtCore.Slot(object, object, object)
  def queueData(self, id, timestamp, frame):
    self.dataQueue.put(frame)
    self.dataEnqueued.emit()
      
  def setDataFormat(self, dataFormat):
    self.disconnectData()
    
    self.dataFormat = dataFormat
    self.dataEngine.connectData(self.dataFormat.name, self.queueData, QtCore.Qt.QueuedConnection)

  def disconnectData(self):
    if self.dataFormat:
      self.dataEngine.disconnectData(self.dataFormat.name, self.queueData)

  def cleanup(self):
    self.unlink()
    self.disconnectData()
      
  def setStatusBar(self, statusBar):
    self.statusBar = statusBar
    
  @staticmethod
  def updateViewBoxLinks():
    if len(DataView.LinkedViewBoxes) == 1:
      v = DataView.LinkedViewBoxes.values()[0]
      v.setXLink(None)
      v.setYLink(None)
      return
    
    v = DataView.LinkedViewBoxes.values()
    
    for i in range(0, len(DataView.LinkedViewBoxes) - 1):
      v[i].setXLink(v[-1])
      v[i].setYLink(v[-1])
      
  ## link() and unlink() are used to synchronize mouse/keyboard events between multiple viewboxes
  def link(self, viewBox):
    DataView.LinkedViewBoxes[self] = viewBox
    
    #print "Number of viewboxes = ", len(DataView.LinkedViewBoxes)    
    DataView.updateViewBoxLinks()
      
  def unlink(self):
    if self in DataView.LinkedViewBoxes:
      del DataView.LinkedViewBoxes[self]
      print "Number of viewboxes = ", len(DataView.LinkedViewBoxes)
      DataView.updateViewBoxLinks()
    
  # Implement in derived class
  @QtCore.Slot()
  def displayData(self):
    pass
    
  @staticmethod
  def getDataView(dataFormat, dataEngine, parent = None):
    if dataFormat.dataType == DataFormat.DATA_2D:
      return DataView2D(dataEngine, dataFormat, parent = parent)
    else:
      return DataView3D(dataEngine, dataFormat, parent = parent)
    
  def setSpanKeyModifier(self, m):
    self.spanKeyModifier = m
    
  def keyPressEvent(self, ev):
    if self.spanKeyModifier is not None and not ev.modifiers() & self.spanKeyModifier:
      ev.ignore()
      return
    
    if ev.key() == QtCore.Qt.Key_Left:
      self.spanSlider.setSliderDown(True)
      if ev.modifiers() & QtCore.Qt.ShiftModifier:
        self.spanSlider.setUpperPosition(self.spanSlider.upperPosition - self.spanSlider.singleStep())
      else:
        self.spanSlider.setLowerPosition(self.spanSlider.lowerPosition - self.spanSlider.singleStep())
      self.spanSlider.setSliderDown(False)
      ev.accept()
    elif ev.key() == QtCore.Qt.Key_Right:
      self.spanSlider.setSliderDown(True)
      if ev.modifiers() & QtCore.Qt.ShiftModifier:
        self.spanSlider.setUpperPosition(self.spanSlider.upperPosition + self.spanSlider.singleStep())
      else:
        self.spanSlider.setLowerPosition(self.spanSlider.lowerPosition + self.spanSlider.singleStep())
      self.spanSlider.setSliderDown(False)
      ev.accept()
    elif ev.key() == QtCore.Qt.Key_Down:
      self.spanSlider.setSliderDown(True)
      if ev.modifiers() & QtCore.Qt.ShiftModifier:
        self.spanSlider.setUpperPosition(self.spanSlider.upperPosition - self.spanSlider.pageStep())
      else:
        self.spanSlider.setLowerPosition(self.spanSlider.lowerPosition - self.spanSlider.pageStep())
      self.spanSlider.setSliderDown(False)
      ev.accept()
    elif ev.key() == QtCore.Qt.Key_Up:
      self.spanSlider.setSliderDown(True)
      if ev.modifiers() & QtCore.Qt.ShiftModifier:
        self.spanSlider.setUpperPosition(self.spanSlider.upperPosition + self.spanSlider.pageStep())
      else:
        self.spanSlider.setLowerPosition(self.spanSlider.lowerPosition + self.spanSlider.pageStep())
      self.spanSlider.setSliderDown(False)
      ev.accept()
    else:
      super(DataView, self).keyPressEvent(ev)

from DataView2D import DataView2D
from DataView3D import DataView3D