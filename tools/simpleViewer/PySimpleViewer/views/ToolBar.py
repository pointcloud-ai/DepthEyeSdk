#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#
from PySide import QtCore, QtGui
from functools import partial
from PySimpleViewer.Dialogs.SelectDepthCameraDialog import SelectDepthCameraDialog
import Voxel

class ToolBar(QtCore.QObject):
    def __init__(self, cameraSystem, toolbar, window, parent = None):
        super(ToolBar, self).__init__(parent)
        self.toolbar = toolbar
        self.cameraSystem = cameraSystem
        self.depthCameraStreamController = window.depthCameraStreamController
        self.items = []
        self.itemDict = {}

        self.toggle_btn = QtGui.QPushButton("Start")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(False)
        self.toggle_btn.clicked.connect(self._toggle_btn_cb)
        toolbar.addWidget(self.toggle_btn)

    def _toggle_btn_cb(self):
        '''print "is checked:", self.toggle_btn.isChecked()'''
        if self.toggle_btn.isChecked():
            self.toggle_btn.setText("STOP")
            self.setDepthCamera(SelectDepthCameraDialog.showDialog(self.cameraSystem))
        else:
            self.toggle_btn.setText("START")
            """self.depthCameraStreamController.disconnectDepthCamera()"""
            self.depthCameraStreamController.resetDepthCamera()

    def setDepthCamera(self, depthCamera):
        if depthCamera:
            self.depthCameraStreamController.setDepthCamera(depthCamera)
            self.depthCameraStreamController.start()

