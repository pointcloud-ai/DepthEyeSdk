#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtGui, QtCore

import pyqtgraph

from pyqtgraph.graphicsItems.PlotDataItem import dataType

import numpy as np

import weakref

class CustomHistogramLUTWidget(pyqtgraph.HistogramLUTWidget):
  
  resetView = QtCore.Signal()
  autoHistogram = QtCore.Signal()
  histogramToggle = QtCore.Signal()
  export = QtCore.Signal()
  
  def __init__(self, parent = None, fillHistogram = True):
    super(CustomHistogramLUTWidget, self).__init__(parent = parent, fillHistogram = fillHistogram)
    self.vb.setMouseEnabled(x=False, y=False) # Disable zoom in viewbox
    self.item.gradientChanged = self.gradientChanged
    
    # Disable right click and other mouse events on gradient
    self.gradient.mouseClickEvent = self.gradientMouseClickEvent 
    #self.plot.setData = self.setData
    
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
      super(CustomHistogramLUTWidget, self).keyPressEvent(ev)

  def gradientMouseClickEvent(self, ev):
    pass
  
  def setImageItem(self, img):
    if self.item.imageItem() is not None:
      self.item.imageItem().sigImageChanged.disconnect(self.imageChanged)
    
    if img is not None:
      self.item.imageItem = weakref.ref(img)
      img.sigImageChanged.connect(self.imageChanged)
    else:
      self.item.imageItem = lambda: None
      
  def setMenu(self, menu):
    self.item.vb.menu = menu
    
  def gradientChanged(self):
    pass
    
  @QtCore.Slot()
  def imageChanged(self, autoLevel=False, autoRange=False):
    h = self.imageItem().getHistogram(bins = 100)
    if h[0] is None:
        return
    self.plot.setData(*h)
    
  def setData(self, *args, **kargs):
    self.updateItems(args[0], args[1])
    self.plot.informViewBoundsChanged()
    self.plot.sigPlotChanged.emit(self.plot)
    
  def updateItems(self, x, y):
    curveArgs = {}
    for k,v in [('pen','pen'), ('shadowPen','shadowPen'), ('fillLevel','fillLevel'), ('fillBrush', 'brush'), ('antialias', 'antialias'), ('connect', 'connect'), ('stepMode', 'stepMode')]:
        curveArgs[v] = self.plot.opts[k]
    
    if curveArgs['pen'] is not None or (curveArgs['brush'] is not None and curveArgs['fillLevel'] is not None):
        self.plot.curve.setData(x=x, y=y, **curveArgs)
        self.plot.curve.show()
    else:
        self.plot.curve.hide()