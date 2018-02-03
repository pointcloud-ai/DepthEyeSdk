#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#
import os
import string
import random
import datetime
import sys

def makePath(p):
    d = os.path.dirname(p)
    try:
        if not os.path.exists(d):
            os.makedirs(d)
    except IOError, e:
        return False

    return True

def generateTemporaryID(size = 6, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getDisplayTime(timedelta):
    t = datetime.timedelta(microseconds = timedelta)

    hours, rem = divmod(t.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    milliseconds = int(t.microseconds/1000)

    if t.days > 0:
        return "%2d days, %.2d:%.2d:%.2d:%.3d" % (t.days, hours, minutes, seconds, milliseconds)
    else:
        return "%.2d:%.2d:%.2d:%.3d" % (hours, minutes, seconds, milliseconds)

def insertToPathVariable(variable, value):
    if not variable in os.environ:
        os.environ[variable] = value
    elif not value in os.environ.get(variable).split(os.pathsep):
        os.environ[variable] = value + os.pathsep + os.environ[variable]

def removeFromPathVaribale(variable, value):
    if variable in os.environ:
        pp = os.environ.get(variable).split(os.pathsep)
        if value in pp:
            pp.remove(value)
        os.environ[variable] = os.pathsep.join(pp)