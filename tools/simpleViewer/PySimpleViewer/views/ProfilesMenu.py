#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#
from PySide import QtGui, QtCore

from functools import partial

import Voxel

class ProfilesMenu(QtGui.QMenu):
  
  def __init__(self, window, parent = None):
    super(ProfilesMenu, self).__init__(parent)
      
    self.window = window
    self.statusBar = window.statusMessage
    self.dataEngine = window.dataEngine
    self.depthCameraStreamController = window.depthCameraStreamController
    
    self.depthCameraStreamController.onDepthCameraSet.connect(self.initMenu)
    
    self.initMenu()
    
    self.setTitle('&Camera Profiles')

  def initMenu(self):
    self.clear()
    
    d = self.depthCameraStreamController.getDepthCamera()
    if not d:
      return
    
    names = sorted(d.getCameraProfileNames().items(), key = lambda x: (d.configFile.getCameraProfile(x[0]).getLocation() << 16) + x[0], reverse = True)
    
    if len(names) == 0:
      return

    cameraProfilesGroup = QtGui.QActionGroup(self, exclusive = True)

    for id, n in names:
      profile = d.configFile.getCameraProfile(id)
      
      if profile:
        if profile.getLocation() == Voxel.ConfigurationFile.IN_CAMERA:
          n += " (HW)"
        a = QtGui.QAction(n, self)
        a.triggered.connect(partial(self.setCameraProfile, name = n, id = id))
        a.setCheckable(True)
        self.addAction(a)

        if d.getCurrentCameraProfileID() == id:
          a.setChecked(True)
        a.setActionGroup(cameraProfilesGroup)
      
    self.addSeparator()

    self.addAction(a)
  
  @QtCore.Slot()
  def setCameraProfile(self, name, id):
    
    d = self.depthCameraStreamController.getDepthCamera()
    
    if d:
      r = d.isRunning()
      
      if r:
        self.depthCameraStreamController.stop()
      
      if not d.setCameraProfile(id):
        QtGui.QMessageBox.critical(self, 'Camera Profile selection', 'Could not select camera profile "' + name + '"')
      
      self.depthCameraStreamController.onDepthCameraSet.emit()
      
      if r:
        self.depthCameraStreamController.start()


