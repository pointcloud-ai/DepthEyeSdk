#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtGui, QtCore
from PySimpleViewer.common.about import *
from PySimpleViewer.Dialogs.AboutDialog import *
from PySimpleViewer.docks.CameraDockWidget import CameraDockWidget
from PySimpleViewer.Dialogs.SelectDepthCameraDialog import SelectDepthCameraDialog
from PySimpleViewer.views.StatusBar import StatusBar
from PySimpleViewer.views.DataViewContainer import DataViewContainer
from PySimpleViewer.views.ProfilesMenu import ProfilesMenu
from PySimpleViewer.views.ToolBar import ToolBar
from PySimpleViewer.models.DepthCameraStreamController import *
from PySimpleViewer.models.DataEngine import *

import Voxel


class MainWindow(QtGui.QMainWindow):
    def __init__(self, cameraSystem):
        super(MainWindow, self).__init__()
        self.baseWindowTitle = "Simple Viewer (v" + VERSION_NUMBER + ")"
        self.setWindowTitle(self.baseWindowTitle)
        '''self.showMaximized()'''

        self.setMinimumWidth(600)
        self.setMinimumHeight(470)

        self.cameraSystem = cameraSystem
        self.depthCameraStreamController = DepthCameraStreamController(self.cameraSystem)
        self.depthCameraStreamController.sourceSelected.connect(self.updateDockViews)
        self.depthCameraStreamController.sourceListChanged.connect(self.updateDockViews)
        self.dataEngine = DataEngine(self.depthCameraStreamController)

        self.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks | QtGui.QMainWindow.VerticalTabs)
        try:
            self.viewer3 = DataViewContainer(self.dataEngine, 'pointcloud')
        except Exception as exceptInst:
            print (exceptInst)
            self.viewer3 = DataViewContainer(self.dataEngine, 'phase')
        self.setCentralWidget(self.viewer3)
        '''self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.RightDockWidgetArea)'''

        self.cameraDockWidget = CameraDockWidget(self.dataEngine)
        self.cameraDockWidget.setDepthCameraStreamController(self.depthCameraStreamController)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.cameraDockWidget)

        self.initStatusBar()

        self.initMenu()
        self.initToolBar()

        self.statusMessage.setProfilesMenu(self.profilesMenu)
        self.cameraDockWidget.setStatusBar(self.statusMessage)
        self.viewer3.setStatusBar(self.statusMessage)
        #self.selectDepthCamera()

    def setDepthCamera(self, depthCamera):
        if depthCamera:
            self.depthCameraStreamController.setDepthCamera(depthCamera)
            self.depthCameraStreamController.start()

    def selectDepthCamera(self):
        devices = self.cameraSystem.scan()
        if len(devices) == 1:
            self.setDepthCamera(self.cameraSystem.connect(devices[0]))
        else:
            ##if SplashDialog.dialog is not NSplashDialog.pyone:
            ##   SplashDialog.dialog.timer.timeout.connect(self.showSelectDepthCameraDialog)
            ##else:
            self.showSelectDepthCameraDialog()

    @QtCore.Slot()
    def showSelectDepthCameraDialog(self):
        self.setDepthCamera(SelectDepthCameraDialog.showDialog(self.cameraSystem, parent=self))

    def initMenu(self):
        exitAction = QtGui.QAction(QtGui.QIcon.fromTheme('exit'), '&Exit application', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        cameraAction = QtGui.QAction(QtGui.QIcon.fromTheme('list'), '&Connect Depth Camera', self)
        cameraAction.setShortcut('Ctrl+C')
        cameraAction.setStatusTip('Select depth camera')
        cameraAction.triggered.connect(self.showSelectDepthCameraDialog)

        disconnectAction = QtGui.QAction(QtGui.QIcon.fromTheme('disconnect'), '&Disconnect Depth Camera', self)
        disconnectAction.setShortcut('Ctrl+D')
        disconnectAction.setStatusTip('Disconnect currect depth camera')
        disconnectAction.triggered.connect(self.disconnectDepthCamera)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(cameraAction)
        fileMenu.addAction(disconnectAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        self.profilesMenu = ProfilesMenu(self)
        menubar.addMenu(self.profilesMenu)

        docks = self.createPopupMenu()
        docks.setTitle('&Windows')
        menubar.addMenu(docks)

        helpAction = QtGui.QAction(QtGui.QIcon.fromTheme('help'), '&Help', self)
        helpAction.setShortcut('Ctrl+H')
        helpAction.setStatusTip('Help about Tools')
        helpAction.setEnabled(False)

        aboutAction = QtGui.QAction(QtGui.QIcon.fromTheme('about'), '&About', self)
        aboutAction.setShortcut('Ctrl+B')
        aboutAction.triggered.connect(self.showAboutDialog)
        aboutAction.setStatusTip('About SimpleViewer')

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(helpAction)
        helpMenu.addSeparator()
        helpMenu.addAction(aboutAction)
        helpMenu.addSeparator()


    def showAboutDialog(self):
        AboutDialog.showDialog(parent = self)

    def initToolBar(self):
        play = self.addToolBar("play control")
        self.toolbar = ToolBar(self.cameraSystem, play, self)

    def initStatusBar(self):
        self.statusMessage = StatusBar(self.dataEngine)
        self.statusMessage.setAddTextFunction(self.getTemperatureStatus, 60)
        self.statusBar().addPermanentWidget(self.statusMessage, 1)
        self.statusBar().setSizeGripEnabled(False)

    def getTemperatureStatus(self):
        # d = self.depthCameraStreamController.getDepthCamera()
        # TODO Identify temperature parameters for each type of depth camera
        return None

    def closeEvent(self, event):
        self.depthCameraStreamController.stop()
        self.dataEngine.stop()
        self.cameraListDockWidget.stopDeviceDetecting()
        '''self.logDockWidget.stop()'''
        event.accept()

    @QtCore.Slot()
    def disconnectDepthCamera(self):
        """self.depthCameraStreamController.disconnectDepthCamera()"""
        self.depthCameraStreamController.resetDepthCamera()

    def updateDeviceConnectStatus(self, connected):
        self.statusMessage.setConnected(connected)

    @QtCore.Slot()
    def updateDockViews(self):
        s = self.depthCameraStreamController.getCurrentSource()
        if s is not None and s.isLiveStream():
            '''self.dataDiagramDockWidget.setVisible(True)'''
            self.updateDeviceConnectStatus(True)
        else:
            self.updateDeviceConnectStatus(False)
            '''self.dataDiagramDockWidget.setVisible(False)'''


