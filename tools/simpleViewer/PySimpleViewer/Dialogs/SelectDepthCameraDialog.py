#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtGui, QtCore

class SelectDepthCameraDialog(QtGui.QDialog):
  def __init__(self, cameraSystem, parent = None):
    super(SelectDepthCameraDialog, self).__init__(parent)

    self.setWindowTitle('Select Depth Camera')
    self.cameraSystem = cameraSystem

    layout = QtGui.QVBoxLayout(self)

    # nice widget for editing the date
    self.listview = QtGui.QListWidget()
    layout.addWidget(self.listview)

    # OK and Cancel buttons
    buttons = QtGui.QDialogButtonBox(self)
    
    self.okButton = QtGui.QPushButton("&Ok", self)
    self.refreshButton = QtGui.QPushButton("&Refresh", self)
    
    self.refreshButton.clicked.connect(self.populateList)
    
    self.listview.setSelectionMode(QtGui.QListWidget.SingleSelection)
        
    buttons.addButton(self.okButton, QtGui.QDialogButtonBox.AcceptRole)
    buttons.addButton(self.refreshButton, QtGui.QDialogButtonBox.ResetRole)
    
    buttons.accepted.connect(self.accept)
    buttons.rejected.connect(self.reject)
    layout.addWidget(buttons)
    
    self.populateList()

  # get current date and time from the dialog
  def getDepthCamera(self):
    return self.cameraSystem.connect(self.devices[self.listview.currentRow()])
  
  @QtCore.Slot()
  def populateList(self):
    self.devices = self.cameraSystem.scan()
    
    names = []
    for d in self.devices:
      names.append(d.description() + " (" + d.id() + ")") ## Assuming that description is present for all devices
    
    self.listview.clear()
    
    if len(names) > 0:
      self.listview.addItems(names)
      self.listview.setCurrentRow(0)
      self.okButton.setEnabled(True)
    else:
      self.okButton.setDisabled(True)
    

  # static method to create the dialog and return (date, time, accepted)
  @staticmethod
  def showDialog(cameraSystem, parent = None):
    dialog = SelectDepthCameraDialog(cameraSystem, parent)
    result = dialog.exec_()
    
    if result == QtGui.QDialog.Accepted:
      return dialog.getDepthCamera()
    else:
      return None