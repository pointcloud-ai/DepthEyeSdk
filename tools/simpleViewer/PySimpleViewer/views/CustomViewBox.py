#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtGui, QtCore

import pyqtgraph

import numpy as np

class CustomViewBox(pyqtgraph.ViewBox):
  
  resetView = QtCore.Signal()
  autoHistogram = QtCore.Signal()
  histogramToggle = QtCore.Signal()
  export = QtCore.Signal()
  
  def __init__(self):
    super(CustomViewBox, self).__init__()
    self.setMouseMode(pyqtgraph.ViewBox.RectMode)
    self.invertY()
    self.setAspectLocked(True)
    
  def mouseDragEvent(self, ev, axis = None):
    ## if axis is specified, event will only affect that axis.
    ev.accept()  ## we accept all buttons
    
    pos = ev.pos()
    lastPos = ev.lastPos()
    dif = pos - lastPos
    dif = dif * -1

    ## Ignore axes if mouse is disabled
    mouseEnabled = np.array(self.state['mouseEnabled'], dtype=np.float)
    mask = mouseEnabled.copy()
    if axis is not None:
      mask[1 - axis] = 0.0

    ## Scale or translate based on mouse button
    if (ev.button() & QtCore.Qt.LeftButton) and (ev.modifiers() & QtCore.Qt.ShiftModifier):
      tr = dif*mask
      tr = self.mapToView(tr) - self.mapToView(pyqtgraph.Point(0,0))
      x = tr.x() if mask[0] == 1 else None
      y = tr.y() if mask[1] == 1 else None
      
      self.translateBy(x = x, y = y)
      self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
    else:
      super(CustomViewBox, self).mouseDragEvent(ev, axis)
      
  def setMenu(self, menu):
    self.menu = menu
    
  def raiseContextMenu(self, ev):
    menu = self.getMenu(ev)
    #self.scene().addParentContextMenus(self, menu, ev) -- Not adding parent's context menus
    menu.popup(ev.screenPos().toPoint())
      
  def keyPressEvent(self, ev):
    if ev.key() == QtCore.Qt.Key_R:
      self.resetView.emit()
      ev.accept()
    elif ev.key() == QtCore.Qt.Key_A:
      self.autoHistogram.emit()
      ev.accept()
    elif ev.key() == QtCore.Qt.Key_H:
      self.histogramToggle.emit()
      ev.accept()
    elif ev.key() == QtCore.Qt.Key_E:
      self.export.emit()
      ev.accept()  
    
    else:
      super(CustomViewBox, self).keyPressEvent(ev)
    