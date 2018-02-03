#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from PySide import QtGui, QtCore
from PySimpleViewer.common.about import *

class AboutDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        super(AboutDialog, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)
        self.setWindowTitle('About SimpleViewer')
        self.setMinimumWidth(400)

        hlayout = QtGui.QHBoxLayout()
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(QtGui.QLabel(SOFTWARE_NAME))
        vlayout.addWidget(QtGui.QLabel(COMPANY_NAME))
        vlayout.addWidget(QtGui.QLabel('Version: ' + VERSION_NUMBER))

        hlayout.addLayout(vlayout)
        layout.addLayout(hlayout)

        self.messageBox = QtGui.QTextBrowser()
        self.messageBox.setText(""" Source and Binary Code Internal Use License Agreement """)

        layout.addWidget(self.messageBox)

        buttons = QtGui.QDialogButtonBox(self)
        self.okButton = QtGui.QPushButton("&OK", self)
        buttons.addButton(self.okButton, QtGui.QDialogButtonBox.AcceptRole)

        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    @staticmethod
    def showDialog(parent = None):
        dialog = AboutDialog(parent)
        result = dialog.exec_()

        return None
