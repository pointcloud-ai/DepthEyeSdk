#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtGui, QtCore

from DataView import DataView

from PySimpleViewer.models.DataEngine import DataFormat

from CustomAction import CustomAction

class DataViewContainer(QtGui.QGroupBox):
  
  def __init__(self, dataEngine, dataFormatName, shouldLinkViewBox = False, showFormatMenu = True, parent = None):
    super(DataViewContainer, self).__init__(parent)
    
    self.dataEngine = dataEngine
    self.statusBar = None
    
    self.shouldLinkViewBox = shouldLinkViewBox
    
    self.setDataFormat(dataFormatName)
    
    if showFormatMenu:
      self.menuActions = []
      self.setContextMenu()
      
      self.dataEngine.statisticsChanged.connect(self.setContextMenu)
      self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
    
  def removeAllActions(self):
    if hasattr(self, 'menuActions'):
      for a in self.menuActions:
        self.removeAction(a)
      self.menuActions = []
    
  def setContextMenu(self):
    self.removeAllActions()
    
    df = self.dataEngine.getDataFormats()
    
    for d in df:
      a = CustomAction(self.dataEngine.dataFormats[d].title, d, self)
      a.triggeredObject.connect(self.setDataFormat)
      self.addAction(a)
      self.menuActions.append(a)
      
  def setStatusBar(self, statusBar):
    self.statusBar = statusBar
    
    if hasattr(self, 'dataView'):
      self.dataView.setStatusBar(self.statusBar)
      
  def setDataFormat(self, dataFormatName):
    
    if not self.dataEngine.dataFormats.has_key(dataFormatName):
      QtGui.QMessageBox('DataView failed', 'Failed to show data of format "' + dataFormatName + '"')
    
    self.dataFormat = self.dataEngine.dataFormats[dataFormatName]
    
    self.setTitle(self.dataFormat.title)
    
    if hasattr(self, 'dataView') and self.dataView.dataFormat.dataType == self.dataFormat.dataType:
      #self.dataView.unlink()
      #QtGui.QWidget().setLayout(self.layout)
      #print 'Linking new data...'
      self.dataView.setDataFormat(self.dataFormat)
    else:
      
      if hasattr(self, 'dataView'):
        self.dataView.cleanup()
        QtGui.QWidget().setLayout(self.layout)
      
      self.layout = QtGui.QVBoxLayout()
      self.dataView = DataView.getDataView(self.dataFormat, self.dataEngine)
      if self.statusBar:
        self.dataView.setStatusBar(self.statusBar)
        
      self.layout.addWidget(self.dataView)
      self.setLayout(self.layout)
      
      if self.dataFormat.dataType == DataFormat.DATA_2D and self.shouldLinkViewBox:
        self.dataView.linkViewBox()
    