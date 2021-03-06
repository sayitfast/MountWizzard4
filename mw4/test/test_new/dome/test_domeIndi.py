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
import unittest.mock as mock

# external packages

from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from indibase.indiBase import Device, Client

# local import
from mw4.dome.domeIndi import DomeIndi
from mw4.dome.dome import DomeSignals


@pytest.fixture(autouse=True, scope='function')
def module_setup_teardown():
    class Test(QObject):
        threadPool = QThreadPool()
        message = pyqtSignal(str, int)
        update1s = pyqtSignal()
    global app
    app = DomeIndi(app=Test(), signals=DomeSignals(), data={})
    yield
    del app


def test_setUpdateConfig_1():
    app.name = ''
    suc = app.setUpdateConfig('test')
    assert not suc


def test_setUpdateConfig_2():
    app.name = 'test'
    app.device = None
    suc = app.setUpdateConfig('test')
    assert not suc


def test_setUpdateConfig_3():
    app.name = 'test'
    app.device = Device()
    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'Test': 1}):
        suc = app.setUpdateConfig('test')
        assert not suc


def test_setUpdateConfig_4():
    app.name = 'test'
    app.device = Device()
    app.UPDATE_RATE = 1
    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'PERIOD_MS': 1}):
        suc = app.setUpdateConfig('test')
        assert suc


def test_setUpdateConfig_5():
    app.name = 'test'
    app.device = Device()
    app.client = Client()
    app.UPDATE_RATE = 0
    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'PERIOD_MS': 1}):
        with mock.patch.object(app.client,
                               'sendNewNumber',
                               return_value=False):
            suc = app.setUpdateConfig('test')
            assert not suc


def test_setUpdateConfig_6():
    app.name = 'test'
    app.device = Device()
    app.client = Client()
    app.UPDATE_RATE = 0
    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'PERIOD_MS': 1}):
        with mock.patch.object(app.client,
                               'sendNewNumber',
                               return_value=True):
            suc = app.setUpdateConfig('test')
            assert suc


def test_updateStatus_1():
    app.device = Device()
    app.client = Client()
    app.client.connected = False

    suc = app.updateStatus()
    assert not suc


def test_updateStatus_2():
    app.device = Device()
    app.client = Client()
    app.client.connected = True

    suc = app.updateStatus()
    assert suc


def test_waitSettlingTime():
    suc = app.waitSettlingAndEmit()
    assert suc


def test_updateNumber_1():
    app.device = None
    suc = app.updateNumber('test', 'test')
    assert not suc


def test_updateNumber_2():
    app.device = Device()
    app.name = ''
    suc = app.updateNumber('test', 'test')
    assert not suc


def test_updateNumber_3():
    app.device = Device()
    app.name = 'test'
    suc = app.updateNumber('test', 'test')
    assert suc


def test_updateNumber_4():
    app.device = Device()
    app.name = 'test'
    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'TEST': 1,
                                         'DOME_ABSOLUTE_POSITION': 2}):
        suc = app.updateNumber('test', 'DOME_ABSOLUTE_POSITION')
        assert suc


def test_updateNumber_5():
    app.device = Device()
    app.device.ABS_DOME_POSITION = {'state': 'test'}
    app.name = 'test'
    app.azimuth = 10
    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'TEST': 1,
                                         'DOME_ABSOLUTE_POSITION': 2}):
        suc = app.updateNumber('test', 'DOME_ABSOLUTE_POSITION')
        assert suc


def test_updateNumber_6():
    app.device = Device()
    app.device.ABS_DOME_POSITION = {'state': 'Busy'}
    app.name = 'test'
    app.azimuth = 10
    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'TEST': 1,
                                         'DOME_ABSOLUTE_POSITION': 2}):
        suc = app.updateNumber('test', 'DOME_ABSOLUTE_POSITION')
        assert suc


def test_updateNumber_7():
    app.device = Device()
    app.device.ABS_DOME_POSITION = {'state': 'test'}
    app.name = 'test'
    app.azimuth = 10
    app.slewing = True
    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'TEST': 1,
                                         'DOME_ABSOLUTE_POSITION': 2}):
        suc = app.updateNumber('test', 'DOME_ABSOLUTE_POSITION')
        assert suc


def test_slewToAltAz_1():
    suc = app.slewToAltAz()
    assert not suc


def test_slewToAltAz_2():
    app.device = Device()
    suc = app.slewToAltAz()
    assert not suc


def test_slewToAltAz_3():
    app.device = Device()
    app.name = 'test'
    suc = app.slewToAltAz()
    assert not suc


def test_slewToAltAz_4():
    app.device = Device()
    app.name = 'test'

    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'DOME_ABSOLUTE_POSITION': 1}):
        suc = app.slewToAltAz()
        assert not suc


def test_slewToAltAz_5():
    app.device = Device()
    app.client = Client()
    app.name = 'test'

    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'DOME_ABSOLUTE_POSITION': 1}):
        with mock.patch.object(app.client,
                               'sendNewNumber',
                               return_value=False):
            suc = app.slewToAltAz()
            assert not suc


def test_slewToAltAz_6():
    app.device = Device()
    app.client = Client()
    app.name = 'test'

    with mock.patch.object(app.device,
                           'getNumber',
                           return_value={'DOME_ABSOLUTE_POSITION': 1}):
        with mock.patch.object(app.client,
                               'sendNewNumber',
                               return_value=True):
            suc = app.slewToAltAz()
            assert suc
