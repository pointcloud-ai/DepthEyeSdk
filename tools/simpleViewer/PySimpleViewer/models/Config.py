#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

import ConfigParser
from PySimpleViewer.common.Common import makePath
from PySimpleViewer.common.about import VERSION_NUMBER
import os
from PySide import QtCore, QtGui

class Config:
    configs = {}

    VIEWER_MAIN_CONFIG = 'viewer.conf'

    def __init__(self, fileName):
        self.fileName = fileName
        makePath(self.fileName)

        self.parser = ConfigParser.RawConfigParser()
        self.parser.optionxform = str
        self.parser.read(self.fileName)

    def copy(self):
        return Config(self.fileName)

    def hasOption(self, section, option):
        try:
            return self.parser.has_option(section, option)
        except Exception, e:
            return False

    def get(self, section, option):
        try:
            return self.parser.get(section, option)
        except Exception, e:
            return False

    def getInt(self, section, option):
        try:
            return self.parser.getint(section, option)
        except Exception, e:
            return False

    def getFloat(self, section, option):
        try:
            return self.parser.getfloat(section, option)
        except Exception, e:
            return False

    def getBoolean(self, section, option):
        try:
            return self.parser.getboolean(section, option)
        except Exception, e:
            return False

    def set(self, section, option, value):
        try:
            if not self.parser.has_section(section):
                self.parser.add_section(section)

            self.parser.set(section, option, value)

            self.parser.write(open(self.fileName, 'w'))
        except Exception, e:
            return False

    def remove(self, section, option):
        if not self.parser.has_section(section):
            return False
        if self.parser.remove_option(section, option):
            self.parser.write(open(self.fileName, 'w'))

    def write(self):
        self.parser.write(open(self.fileName, 'w'))

    @staticmethod
    def getConfig(name, basePath = None):
        if basePath is None:
            homeDrive = os.getenv('HOMEDRIVE')
            homePath = os.getenv('HOMEPATH')
            if homeDrive is None or homePath is None:
                basePath = os.path.expanduser('~/.Voxel/viewer-' + VERSION_NUMBER)
            else:
                basePath = homeDrive + homePath + '/.Voxel/viewer-' + VERSION_NUMBER

            if len(basePath) > 0:
                f = basePath + os.sep + name
                if Config.configs.has_key(name):
                    return Config.configs[name]
                else:
                    c = Config(f)
                    Config.configs[name] = c
                    return c
                    '''should be Confid.configs[name]???'''
            else:
                QtGui.QMessageBox.critical(None, 'Path failed', 'Failed to get configuration file')
                return False
