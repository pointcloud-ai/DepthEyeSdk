#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtGui, QtCore
from PySimpleViewer.MainWindow import MainWindow
from PySimpleViewer.common.about import *
import os, sys
import Voxel

app = QtGui.QApplication(sys.argv)

Voxel.cvar.logger.setDefaultLogLevel(Voxel.LOG_WARNING)
cameraSystem = Voxel.CameraSystem()

window = None
def createWindow():
    global window
    if window == None:
        window = MainWindow(cameraSystem)
    return

createWindow()
window.show()
app.exec_()

del cameraSystem
sys.exit(0)
