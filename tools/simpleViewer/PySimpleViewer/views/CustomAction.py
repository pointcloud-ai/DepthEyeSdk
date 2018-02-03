#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtCore, QtGui

class CustomAction(QtGui.QAction):
  
  triggeredObject = QtCore.Signal(object)
  
  def __init__(self, title, data, parent = None):
    super(CustomAction, self).__init__(title, parent)
    
    self.data = data
    
    self.triggered.connect(self.triggerObject)
    
  @QtCore.Slot(bool)
  def triggerObject(self, checked = True):
    self.triggeredObject.emit(self.data)