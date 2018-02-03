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

from PySimpleViewer.models.DataQueue import DataQueue

from PySimpleViewer.models.DataEngine import *

from DataView import DataView

from CustomViewBox import CustomViewBox
from CustomHistogramLUTWidget import CustomHistogramLUTWidget

from QxtSpanSlider import QxtSpanSlider

import weakref

class DataView2DMenu(QtGui.QMenu):
  
  def __init__(self, parent):
    super(DataView2DMenu, self).__init__(parent)
    
    self.resetAction = QtGui.QAction(QtGui.QIcon.fromTheme('reset'), '&Reset view', parent)
    self.resetAction.setShortcut('R')
    self.resetAction.triggered.connect(parent.resetView)
    self.addAction(self.resetAction)
    
    self.autoLevelsAction = QtGui.QAction(QtGui.QIcon.fromTheme('auto'), 'Upd&ate Thresholds', parent)
    self.autoLevelsAction.setShortcut('A')
    self.autoLevelsAction.triggered.connect(parent.autoLevels)
    self.addAction(self.autoLevelsAction)
    
    self.histogramAction = QtGui.QAction(QtGui.QIcon.fromTheme('statistics'), '&Histogram', parent)
    self.histogramAction.setCheckable(True)
    self.histogramAction.setShortcut('H')
    self.histogramAction.setChecked(parent.histogramVisible)
    self.histogramAction.triggered.connect(parent.toggleHistogramView)
    self.addAction(self.histogramAction)
    
    self.addSeparator()
    
    self.exportAction = QtGui.QAction(QtGui.QIcon().fromTheme('export'), '&Export Image', parent)
    self.exportAction.setShortcut('E')
    self.exportAction.triggered.connect(parent.exportImage)
    self.addAction(self.exportAction)

class DataView2D(DataView):
  
  dataAvailable = QtCore.Signal()
  
  HISTOGRAM_THRESHOLD = 10
  
  def __init__(self, dataEngine, dataFormat, sizeRect = None, parent = None):
    DataView.__init__(self, dataEngine, dataFormat, parent)
    
    self.updateCount = 0
    
    self.graphicsWidget = pyqtgraph.GraphicsLayoutWidget()
    
    hlayout = QtGui.QHBoxLayout()
    self.viewBox = CustomViewBox()
    self.graphicsWidget.addItem(self.viewBox)
    
    self.viewBox.sigRangeChanged.connect(self.computeChangedRange)
    
    self.imageItem = pyqtgraph.ImageItem()
    self.viewBox.addItem(self.imageItem)
    
    if sizeRect:
      self.viewBox.setRange(sizeRect)
      
    hlayout.addWidget(self.graphicsWidget)
    self.histogramLUTWidget = CustomHistogramLUTWidget()
    hlayout.addWidget(self.histogramLUTWidget)
    
    self.histogramLUTWidget.setImageItem(self.imageItem)
    
    self.viewBox.resetView.connect(self.resetView)
    self.histogramLUTWidget.resetView.connect(self.resetView)
    
    self.viewBox.autoHistogram.connect(self.autoLevels)
    self.histogramLUTWidget.autoHistogram.connect(self.autoLevels)
    
    self.viewBox.histogramToggle.connect(self.toggleHistogramView)
    self.histogramLUTWidget.histogramToggle.connect(self.toggleHistogramView)
    
    self.viewBox.export.connect(self.exportImage)
    self.histogramLUTWidget.export.connect(self.exportImage)
      
    self.layout = QtGui.QVBoxLayout()
    self.layout.addLayout(hlayout)
    
    hlayout = QtGui.QHBoxLayout()
    self.spanLabel = QtGui.QLabel('Threshold:')
    hlayout.addWidget(self.spanLabel)
    self.spanSlider = QxtSpanSlider()
    self.spanSlider.lowerPositionChanged.connect(self.updateLowerLevel)
    self.spanSlider.upperPositionChanged.connect(self.updateUpperLevel)
    hlayout.addWidget(self.spanSlider)
    self.layout.addLayout(hlayout)
    self.setLayout(self.layout)
    
    self.setFocusProxy(self.graphicsWidget)
    
    self.setDataFormat(dataFormat)
    
    self.graphicsWidget.scene().sigMouseMoved.connect(self.getMousePosition)
    self.graphicsWidget.scene().sigMouseClicked.connect(self.sendClickPosition)
    
    self.depthCameraController = dataEngine.getDepthCameraController()
    self.depthCameraController.started.connect(self.streamStarted)
    
    self.histogramVisible = True
    self.toggleHistogramView()
    
    m1 = DataView2DMenu(self)
    m2 = DataView2DMenu(self)
    self.viewBox.setMenu(m1)
    self.histogramLUTWidget.setMenu(m2)
    m1.histogramAction.toggled.connect(m2.histogramAction.setChecked)
    m2.histogramAction.toggled.connect(m1.histogramAction.setChecked)
    
    self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    
  def computeChangedRange(self):
    range = self.viewBox.viewRect()
    isec = range.intersected(self.imageItem.boundingRect());
    #print isec.x(), isec.y(), isec.x() + isec.width() - 1, isec.y() + isec.height() - 1
    DataView.communicator.viewRangeChanged.emit(isec.x(), isec.y(), isec.x() + isec.width() - 1, isec.y() + isec.height() - 1)
    
  @QtCore.Slot()
  def resetView(self):
    self.viewBox.autoRange()
    
    if self.dataFormat is None:
      return
    
    self._setDataFormat(self.dataFormat)
    self.autoLevels()
    
    # Reset all linked views
    if self in DataView.LinkedViewBoxes.keys():
      for i in DataView.LinkedViewBoxes.keys():
        if i != self:
          i.autoLevels()
          
  def exportImage(self):
    image = self.imageItem.getPixmap()
    
    if image is None:
      QtGui.QMessageBox.critical(self, 'Blank Image', 'There is no image to export.')
      return
    
    #filter = ["*." + str(f) for f in QtGui.QImageWriter.supportedImageFormats()]
    
    filter = ['*.png', '*.jpg']
    
    filename, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save Image Snapshot', filter = "Image files (" + ' '.join(filter) + ")")
    
    if filename:
      if not image.toImage().save(filename):
        QtGui.QMessageBox.critical(self, 'Save Image Failed', 'Failed to save image to "' + filename + '".')
        return
    
  def autoLevels(self):
    
    b, h = self.imageItem.getHistogram(bins = 100)
    
    if h is None or b is None:
      return
    
    h = (h - DataView2D.HISTOGRAM_THRESHOLD).clip(0)
    
    i = np.nonzero(h)
    
    self.updateImageLevels(b[i[0][0]], b[i[0][-1]])
    
  def setDataFormat(self, dataFormat):
    self._setDataFormat(dataFormat)
    self.updateCount = 0
    
  def _setDataFormat(self, dataFormat):
    super(DataView2D, self).setDataFormat(dataFormat)
    if self.dataFormat.isDepthType:
      s = self.dataEngine.depthCameraController.getCurrentSource()
    
      if s is not None:
        d = s.getDepthScalingFactor()
        self.dataFormat.setScalingFactor(d)
    
    self.levels = [self.dataFormat.levels[0]*self.dataFormat.scalingFactor, self.dataFormat.levels[1]*self.dataFormat.scalingFactor]
    self.histogramLUTWidget.gradient.setColorMap(self.dataFormat.cmap)
    self.imageItem.setLookupTable(self.dataFormat.colorMap)
    self.histogramLUTWidget.setHistogramRange(self.levels[0], self.levels[1])
    self.histogramLUTWidget.setLevels(self.levels[0], self.levels[1])

    if isinstance(self.dataFormat.scalingFactor, int):
      self.spanSlider.setRange(self.levels[0], self.levels[1])
      self.spanSlider.setSpan(self.levels[0], self.levels[1])
    else:
      self.spanSlider.setFloatRange(self.levels[0], self.levels[1], self.dataFormat.scalingFactor)
    
    
  def sendClickPosition(self, ev):
    if ev.button() == QtCore.Qt.LeftButton and ev.modifiers() & QtCore.Qt.ControlModifier: # Alt + Left click?
      DataView.communicator.setCurrentPoint2D.emit(self.imageItem.mapFromScene(ev.scenePos()))
    elif ev.button() == QtCore.Qt.LeftButton and ev.modifiers() & QtCore.Qt.ShiftModifier: # Alt + Left click?
      DataView.communicator.setShiftClickPoint2D.emit(self.imageItem.mapFromScene(ev.scenePos()))
    
  def linkViewBox(self):
    self.link(self.viewBox)
    
  def unlink(self):
    self.viewBox.unregister()
    super(DataView2D, self).unlink()
    
  def getMousePosition(self, pos):
    p = self.imageItem.mapFromScene(pos)
    
    frameSize = self.dataEngine.frameSize
    
    if frameSize is not None:
      if p.x() < 0 or p.x() >= frameSize[0] or p.y() < 0 or p.y() >= frameSize[1]:
        return
      
      point = [int(p.x()), int(p.y())]
    
      if self.statusBar:
        self.statusBar.setPoint(point)
  
  @QtCore.Slot()
  def streamStarted(self):
    self.updateCount = 0
      
  def getLevels(self):
    if self.histogramVisible:
      return self.histogramLUTWidget.getLevels()
    else:
      return self.levels
    
  def toggleHistogramView(self):
    if self.histogramVisible:
      self.spanSlider.show()
      self.spanLabel.show()
      self.levels = list(self.histogramLUTWidget.getLevels())
      self.histogramLUTWidget.setImageItem(None)
      self.histogramLUTWidget.hide()
      
      if isinstance(self.dataFormat.scalingFactor, int):
        self.spanSlider.setSpan(self.levels[0], self.levels[1])
      else:
        self.spanSlider.setSpan(self.levels[0]/self.dataFormat.scalingFactor, self.levels[1]/self.dataFormat.scalingFactor)
      
      self.histogramVisible = False
    else:
      self.histogramLUTWidget.show()
      self.histogramLUTWidget.setImageItem(self.imageItem)
      self.spanSlider.hide()
      self.spanLabel.hide()
      self.histogramLUTWidget.setLevels(self.levels[0], self.levels[1])
      self.histogramVisible = True
      
    self.resetView()
    
  @QtCore.Slot()
  def displayData(self):
    self.updateCount = self.updateCount + 1
    d = self.dataQueue.tryGet()
    
    if d is not None:
      self.imageItem.setImage(d, levels = self.getLevels())
      
      if self.updateCount == 1:
        self.resetView()
    
  @QtCore.Slot(int)
  def updateLowerLevel(self, lower):
    if isinstance(self.dataFormat.scalingFactor, int):
      self.levels[0] = float(lower)
    else:
      self.levels[0] = lower*self.dataFormat.scalingFactor
    self.imageItem.setLevels(self.levels)
    self.histogramLUTWidget.setLevels(self.levels[0], self.levels[1])
    DataView.communicator.thresholdsChanged.emit(self.dataFormat.name, self.levels[0], self.levels[1])
    
  @QtCore.Slot(int)
  def updateUpperLevel(self, upper):
    if isinstance(self.dataFormat.scalingFactor, int):
      self.levels[1] = float(upper)
    else:
      self.levels[1] = upper*self.dataFormat.scalingFactor
    self.imageItem.setLevels(self.levels)
    self.histogramLUTWidget.setLevels(self.levels[0], self.levels[1])
    DataView.communicator.thresholdsChanged.emit(self.dataFormat.name, self.levels[0], self.levels[1])
    
  def updateImageLevels(self, lower, upper):
    self.levels[0] = float(lower)
    self.levels[1] = float(upper)
    
    if isinstance(self.dataFormat.scalingFactor, int):
      self.spanSlider.setSpan(self.levels[0], self.levels[1])
    else:
      self.spanSlider.setSpan(self.levels[0]/self.dataFormat.scalingFactor, self.levels[1]/self.dataFormat.scalingFactor)
        
    self.histogramLUTWidget.setLevels(self.levels[0], self.levels[1])
    self.imageItem.setLevels(self.levels)
    DataView.communicator.thresholdsChanged.emit(self.dataFormat.name, self.levels[0], self.levels[1])