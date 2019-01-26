############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.7
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
###########################################################
# standard libraries
import unittest.mock as mock
import logging
import pytest
# external packages
import PyQt5.QtGui
import PyQt5.QtWidgets
import PyQt5.uic
import PyQt5.QtTest
import PyQt5.QtCore
# local import
from mw4 import mainApp

test = PyQt5.QtWidgets.QApplication([])
mwGlob = {'workDir': '.',
          'configDir': './mw4/test/config',
          'dataDir': './mw4/test/config',
          'modeldata': 'test',
          }

'''
@pytest.fixture(autouse=True, scope='function')
def module_setup_teardown():
    global spy
    global app

    app = mainApp.MountWizzard4(mwGlob=mwGlob)
    spy = PyQt5.QtTest.QSignalSpy(app.message)
    yield
    spy = None
    app = None
'''
app = mainApp.MountWizzard4(mwGlob=mwGlob)
spy = PyQt5.QtTest.QSignalSpy(app.message)


def test_setLoggingLevel1(qtbot):
    app.mainW.ui.loglevelDebug.setChecked(True)
    app.mainW.setLoggingLevel()
    val = logging.getLogger().getEffectiveLevel()
    assert val == 10


def test_setLoggingLevel2(qtbot):
    app.mainW.ui.loglevelInfo.setChecked(True)
    app.mainW.setLoggingLevel()
    val = logging.getLogger().getEffectiveLevel()
    assert val == 20


def test_setLoggingLevel3(qtbot):
    app.mainW.ui.loglevelWarning.setChecked(True)
    app.mainW.setLoggingLevel()
    val = logging.getLogger().getEffectiveLevel()
    assert val == 30


def test_setLoggingLevel4(qtbot):
    app.mainW.ui.loglevelError.setChecked(True)
    app.mainW.setLoggingLevel()
    val = logging.getLogger().getEffectiveLevel()
    assert val == 40


def test_setLoggingLevelIB1(qtbot):
    app.mainW.ui.loglevelDebugIB.setChecked(True)
    app.mainW.setLoggingLevelIB()
    val = logging.getLogger('indibase').getEffectiveLevel()
    assert val == 10


def test_setLoggingLevelIB2(qtbot):
    app.mainW.ui.loglevelInfoIB.setChecked(True)
    app.mainW.setLoggingLevelIB()
    val = logging.getLogger('indibase').getEffectiveLevel()
    assert val == 20


def test_setLoggingLevelIB3(qtbot):
    app.mainW.ui.loglevelWarningIB.setChecked(True)
    app.mainW.setLoggingLevelIB()
    val = logging.getLogger('indibase').getEffectiveLevel()
    assert val == 30


def test_setLoggingLevelIB4(qtbot):
    app.mainW.ui.loglevelErrorIB.setChecked(True)
    app.mainW.setLoggingLevelIB()
    val = logging.getLogger('indibase').getEffectiveLevel()
    assert val == 40


def test_setLoggingLevelMC1(qtbot):
    app.mainW.ui.loglevelDebugMC.setChecked(True)
    app.mainW.setLoggingLevelMC()
    val = logging.getLogger('mountcontrol').getEffectiveLevel()
    assert val == 10


def test_setLoggingLevelMC2(qtbot):
    app.mainW.ui.loglevelInfoMC.setChecked(True)
    app.mainW.setLoggingLevelMC()
    val = logging.getLogger('mountcontrol').getEffectiveLevel()
    assert val == 20


def test_setLoggingLevelMC3(qtbot):
    app.mainW.ui.loglevelWarningMC.setChecked(True)
    app.mainW.setLoggingLevelMC()
    val = logging.getLogger('mountcontrol').getEffectiveLevel()
    assert val == 30


def test_setLoggingLevelMC4(qtbot):
    app.mainW.ui.loglevelErrorMC.setChecked(True)
    app.mainW.setLoggingLevelMC()
    val = logging.getLogger('mountcontrol').getEffectiveLevel()
    assert val == 40
