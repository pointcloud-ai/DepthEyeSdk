#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtGui, QtCore

from PySimpleViewer.views.DataViewContainer import DataViewContainer

#from PyVoxelViewer.views.PhaseViewer import PhaseViewer

class CameraDockWidget(QtGui.QDockWidget):
  def __init__(self, dataEngine):
    QtGui.QDockWidget.__init__(self)
    self.setMinimumWidth(180)
    
    self.scroller = QtGui.QScrollArea()
    
    self.dataEngine = dataEngine
    
    self.layout = QtGui.QVBoxLayout()
    '''self.layout = QtGui.QHBoxLayout()'''
    
    self.viewer1 = DataViewContainer(dataEngine, 'phase', shouldLinkViewBox = True)
    self.layout.addWidget(self.viewer1)
    
    self.viewer2 = DataViewContainer(dataEngine, 'amplitude', shouldLinkViewBox = True)
    self.layout.addWidget(self.viewer2)

    self.layout.addStretch()
    
    self.scroller.setLayout(self.layout)
    
    self.setWidget(self.scroller)
    
  def setStatusBar(self, statusBar):
    self.viewer1.setStatusBar(statusBar)
    self.viewer2.setStatusBar(statusBar)
    
  def onDepthCameraSet(self):
    self.setWindowTitle(self.depthCameraStreamController.getDepthCamera().id())
    
  def setDepthCameraStreamController(self, depthCameraStreamController):
    self.depthCameraStreamController = depthCameraStreamController
    self.depthCameraStreamController.onDepthCameraSet.connect(self.onDepthCameraSet)
