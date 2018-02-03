#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtCore, QtGui

class ClickableLabel(QtGui.QLabel):
  
  clicked = QtCore.Signal()
  
  def __init__(self, parent = None):
    super(ClickableLabel, self).__init__(parent)
    
  def mouseReleaseEvent(self, ev):
    self.clicked.emit()