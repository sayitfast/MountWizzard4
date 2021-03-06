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
# Python  v3.7.5
#
# Michael Würtenberger
# (c) 2019
#
# Licence APL2.0
#
###########################################################
# standard libraries
import pytest
from queue import Queue

# external packages
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

# local import
from mw4.gui.messageW import MessageWindow


@pytest.fixture(autouse=True, scope='function')
def module_setup_teardown():
    global Test

    class Test(QObject):
        config = {'mainW': {}}
        update1s = pyqtSignal()
        messageQueue = Queue()

    yield
    del Test


def test_initConfig_1(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    suc = app.initConfig()
    assert suc


def test_initConfig_2(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    app.app.config['messageW'] = {'winPosX': 10000}
    suc = app.initConfig()
    assert suc


def test_initConfig_3(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    app.app.config['messageW'] = {'winPosY': 10000}
    suc = app.initConfig()
    assert suc


def test_storeConfig_1(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    if 'messageW' in app.app.config:
        del app.app.config['messageW']
    suc = app.storeConfig()
    assert suc


def test_storeConfig_2(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    app.app.config['messageW'] = {}
    suc = app.storeConfig()
    assert suc


def test_closeEvent_1(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    app.closeEvent(QCloseEvent())


def test_clearWindow_1(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    suc = app.clearWindow()
    assert suc


def test_writeMessage_1(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    suc = app.writeMessage()
    assert suc


def test_writeMessage_2(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    app.app.messageQueue.put(('test', 0))
    suc = app.writeMessage()
    assert suc


def test_writeMessage_3(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    app.app.messageQueue.put(('test', -1))
    suc = app.writeMessage()
    assert suc


def test_writeMessage_4(qtbot):
    app = MessageWindow(app=Test())
    qtbot.addWidget(app)

    app.app.messageQueue.put(('test', 10))
    suc = app.writeMessage()
    assert suc
