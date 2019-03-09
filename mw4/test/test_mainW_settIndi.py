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
from mw4.test.test_setupQt import setupQt


@pytest.fixture(autouse=True, scope='module')
def module_setup_teardown():
    global app, spy, mwGlob, test
    app, spy, mwGlob, test = setupQt()
    yield


def test_initConfig_1():
    app.config['mainW'] = {}
    suc = app.mainW.initConfig()
    assert suc


def test_initConfig_2():
    del app.config['mainW']
    suc = app.mainW.initConfig()
    assert suc


def test_storeConfig_1():
    suc = app.storeConfig()
    assert suc


def test_removePrefix_1():
    text = 'test is it'
    pre = 'test'
    val = app.mainW._removePrefix(text, pre)
    assert val == 'is it'


def test_removePrefix_2():
    text = 'testis it'
    pre = 'test'
    val = app.mainW._removePrefix(text, pre)
    assert val == 'is it'


def test_removePrefix_3():
    text = 'test   is it  '
    pre = 'test'
    val = app.mainW._removePrefix(text, pre)
    assert val == 'is it'


def test_indiMessage_1(qtbot):
    app.mainW.ui.indiMessage.setChecked(False)
    device = 'test'
    text = '[WARNING]'

    with qtbot.assertNotEmitted(app.message):
        suc = app.mainW.indiMessage(device, text)
        assert not suc


def test_indiMessage_2(qtbot):
    app.mainW.ui.indiMessage.setChecked(True)
    device = 'test'
    text = '[WARNING] this is a test'
    with qtbot.waitSignal(app.message) as blocker:
        suc = app.mainW.indiMessage(device, text)
        assert suc
    assert ['test -> this is a test', 0] == blocker.args


def test_indiMessage_3(qtbot):
    app.mainW.ui.indiMessage.setChecked(True)
    device = 'test'
    text = '[ERROR] this is a test'
    with qtbot.waitSignal(app.message) as blocker:
        suc = app.mainW.indiMessage(device, text)
        assert suc
    assert ['test -> this is a test', 2] == blocker.args
