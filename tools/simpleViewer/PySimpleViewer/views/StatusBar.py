#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtCore, QtGui

from collections import OrderedDict


import threading
import Voxel

import numpy as np

import math

import sys

from PySimpleViewer.models.Config import Config



from PySimpleViewer.views.ClickableLabel import ClickableLabel

class StatusBar(QtGui.QWidget):
  
  dataAvailable = QtCore.Signal()
  
  def __init__(self, dataEngine):
    super(StatusBar, self).__init__()
    
    self.dataEngine = dataEngine
    '''
    self.calibrationStatus = ClickableLabel()
    self.calibrationStatus.clicked.connect(self.openCalibrationWizard)
    
    # Calibration check setup
    self.depthCameraController = self.dataEngine.depthCameraController
    self.depthCameraController.onDepthCameraSet.connect(self.prepareCalibrationCheck)
    self.prepareCalibrationCheck()
    self.checkCalibration()
    '''
    self.enableStatistics = QtGui.QCheckBox('Temporal Statistics')
    self.enableStatistics.setChecked(True)
    self.isStatisticsEnabled = True
    self.enableStatistics.stateChanged.connect(self.controlStatistics)
    self.deviceConnectStatus = QtGui.QLabel('Device disconnected')
    '''
    self.tiLogo = QtGui.QLabel(self)
    pix = QtGui.QPixmap(':/Ti_hz_2c_pos_rgb_png_small.png')
    pix = pix.scaledToHeight(20, QtCore.Qt.SmoothTransformation)
    self.tiLogo.setPixmap(pix)
    '''
    self.status = QtGui.QLabel()
    self.status.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    
    layout = QtGui.QHBoxLayout()
    layout.addWidget(self.deviceConnectStatus)
    '''layout.addWidget(self.calibrationStatus)'''
    layout.addWidget(self.enableStatistics)
    layout.addWidget(self.status)
    '''layout.addWidget(self.tiLogo)'''
    self.setLayout(layout)
    self.deg = chr(0260)
    
    self.averageFactor = 0.02
    
    self.point = None
    self.addText = None
    self.text = None
    
    self.status.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    
    font = QtGui.QFont("Monospace")
    font.setStyleHint(QtGui.QFont.TypeWriter);
    font.setPointSize(9)
    
    self.status.setFont(font)
    #self.setStyleSheet("font: monospace; font-size: small;")
    
    self.dataEngine.connectData("depth", self.setData, QtCore.Qt.QueuedConnection)
    
    self.dataAvailable.connect(self.updateStatusBar, QtCore.Qt.QueuedConnection)
    
    self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    
    c = Config.getConfig(Config.VIEWER_MAIN_CONFIG)
    
    if c.hasOption('statistics', 'enabled'):
      self.enableStatistics.setChecked(c.getBoolean('statistics', 'enabled'))
  
  def setProfilesMenu(self, profilesMenu):
    self.profilesMenu = profilesMenu
    
  @QtCore.Slot(object)
  def controlStatistics(self, state):
    if state == True or state == QtCore.Qt.Checked:
      self.dataEngine.enableStatistics()
      self.isStatisticsEnabled = True
    elif state == QtCore.Qt.Unchecked:
      self.dataEngine.disableStatistics()
      self.isStatisticsEnabled = False
      
    c = Config.getConfig(Config.VIEWER_MAIN_CONFIG)
    c.set('statistics', 'enabled', self.isStatisticsEnabled)
    
  def setPoint(self, point):
    self.point = point
    self.setData()

  @QtCore.Slot()
  def updateAdditionalText(self):
    if self.addTextFunction:
      self.addText = self.addTextFunction()
      self.setData()
    
  def setAddTextFunction(self, addTextFunction, timing):
    self.addTextFunction = addTextFunction
    self.timing = timing
    
    if hasattr(self, 'updateTimer'):
      self.updateTimer.stop()
      
    self.updateTimer = QtCore.QTimer(self)

    self.updateTimer.timeout.connect(self.updateAdditionalText)
    
    self.updateTimer.start(timing*1000)

  @QtCore.Slot(object, object, object)
  def setData(self, id = 0, timestamp = 0, frame = None):
    
    if not self.point:
      return
    
    if not self.dataEngine.data.has_key('phase') or not self.dataEngine.data.has_key('amplitude') \
      or not self.dataEngine.data.has_key('depth'):
      return
    
    s = self.dataEngine.data['depth'].shape
    
    if self.point[0] < 0 or self.point[1] < 0 or self.point[0] >= s[0] or self.point[1] >= s[1]:
      self.point = None
      return
    
    depth = self.dataEngine.data['depth'][self.point[0]][self.point[1]]

    a = self.dataEngine.data['amplitude'][self.point[0]][self.point[1]]
    p = self.dataEngine.data['phase'][self.point[0]][self.point[1]]
    amb = self.dataEngine.data['ambient'][self.point[0]][self.point[1]]
    flags = self.dataEngine.data['flags'][self.point[0]][self.point[1]]
    
    self.text = "@(%d, %d) -> Amplitude: %04d, Phase: %04d, Ambient: %02d, Flags: %02d, Z: %07.4fm"%(self.point[0], self.point[1], a, p, amb, flags, depth)
    
    if self.addText:
      self.text = self.text + ", " + self.addText
      
    self.dataAvailable.emit()

  @QtCore.Slot()
  def updateStatusBar(self):
    if self.text:
      self.status.setText(unicode(self.text))
      
  def setConnected(self, status):
    if status:
      self.deviceConnectStatus.setText('Device Connected')
    else:
      self.deviceConnectStatus.setText('Device Disconnected')
      