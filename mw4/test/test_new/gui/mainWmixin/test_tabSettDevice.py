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
from unittest import mock
import logging

# external packages
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import pyqtSignal
from mountcontrol.qtmount import Mount
from skyfield.toposlib import Topos

# local import
from mw4.gui.mainWmixin.tabSettDevice import SettDevice
from mw4.gui.widgets.main_ui import Ui_MainWindow
from mw4.gui.widget import MWidget
from mw4.environment.sensorWeather import SensorWeather
from mw4.environment.onlineWeather import OnlineWeather
from mw4.environment.directWeather import DirectWeather
from mw4.environment.skymeter import Skymeter
from mw4.cover.flipflat import FlipFlat
from mw4.imaging.filter import Filter
from mw4.imaging.camera import Camera
from mw4.imaging.focuser import Focuser
from mw4.dome.dome import Dome
from mw4.powerswitch.pegasusUPB import PegasusUPB
from mw4.telescope.telescope import Telescope
from mw4.astrometry.astrometry import Astrometry
from mw4.powerswitch.kmRelay import KMRelay
from mw4.measure.measure import MeasureData
from mw4.remote.remote import Remote
from mw4.base.loggerMW import CustomLogger
from mw4.gui.devicePopupW import DevicePopup


@pytest.fixture(autouse=True, scope='function')
def module_setup_teardown(qtbot):
    global ui, widget, Test, Test1, app

    class Test1(QObject):
        mount = Mount()
        update1s = pyqtSignal()
        update10s = pyqtSignal()
        threadPool = QThreadPool()

    class Test(QObject):
        config = {'mainW': {}}
        threadPool = QThreadPool()
        update1s = pyqtSignal()
        message = pyqtSignal(str, int)
        mount = Mount()
        mount.obsSite.location = Topos(latitude_degrees=20,
                                       longitude_degrees=10,
                                       elevation_m=500)
        sensorWeather = SensorWeather(app=Test1())
        onlineWeather = OnlineWeather(app=Test1())
        directWeather = DirectWeather(app=Test1())
        skymeter = Skymeter(app=Test1())
        cover = FlipFlat(app=Test1())
        filter = Filter(app=Test1())
        camera = Camera(app=Test1())
        focuser = Focuser(app=Test1())
        dome = Dome(app=Test1())
        power = PegasusUPB(app=Test1())
        astrometry = Astrometry(app=Test1())
        relay = KMRelay()
        measure = MeasureData(app=Test1())
        remote = Remote(app=Test1())
        telescope = Telescope(app=Test1())

    widget = QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(widget)

    app = SettDevice(app=Test(), ui=ui,
                     clickable=MWidget().clickable,
                     change=MWidget().changeStyleDynamic)
    app.close = MWidget().close
    app.deleteLater = MWidget().deleteLater
    app.deviceStat = dict()
    app.log = CustomLogger(logging.getLogger(__name__), {})
    app.threadPool = QThreadPool()
    app.config = dict()
    app.BACK_NORM = '#000000'

    qtbot.addWidget(app)

    yield

    del widget, ui, Test, Test1, app


def test_findIndexValue_1():
    val = app.findIndexValue(ui=app.ui.domeDevice,
                             searchString='dome')
    assert val == 0


def test_initConfig_1():
    app.config['mainW'] = {}
    suc = app.initConfig()
    assert suc


def test_initConfig_2():
    suc = app.initConfig()
    assert suc


def test_storeConfig_1():
    suc = app.storeConfig()
    assert suc


def test_storeConfig_2():
    app.driversData['dome'] = {}
    suc = app.storeConfig()
    assert suc


def test_setupDeviceGui_1():
    suc = app.setupDeviceGui()
    assert suc


def test_setupDeviceGui_2():
    class Test:
        pass

    app.drivers['dome']['class'] = Test()
    suc = app.setupDeviceGui()
    assert suc


def test_setupPopUp_1():
    class Test1:
        @staticmethod
        def x():
            return 0

        @staticmethod
        def y():
            return 0

    def Sender():
        return ui.cameraSetup

    def default():
        return 0

    app.sender = Sender
    app.pos = Test1
    app.height = default
    app.width = default
    with mock.patch.object(DevicePopup,
                           'exec_',
                           return_value=False):
        suc = app.setupPopUp()
        assert not suc


def test_dispatchStopDriver_1():
    suc = app.dispatchStopDriver(driver='dome')
    assert not suc


def test_dispatchStopDriver_2():
    app.drivers['dome']['uiDropDown'].setItemText(0, 'test')
    suc = app.dispatchStopDriver(driver='dome')
    assert suc


def test_dispatchStopDriver_3():
    app.drivers['dome']['class'].name = 'dome'
    suc = app.dispatchStopDriver(driver='dome')
    assert not suc


def test_dispatchConfigDriver_1():
    suc = app.dispatchConfigDriver(driver=None)
    assert not suc


def test_dispatchConfigDriver_2():
    suc = app.dispatchConfigDriver(driver='dome')
    assert suc


def test_dispatchStartDriver_1():
    suc = app.dispatchStartDriver(driver=None)
    assert not suc


def test_dispatchStartDriver_2():
    suc = app.dispatchStartDriver(driver='dome')
    assert not suc


def test_enableRelay_1(qtbot):
    app.ui.relayDevice.setCurrentIndex(0)
    with mock.patch.object(app.app.relay,
                           'stopCommunication',
                           return_value=None):
        suc = app.dispatch()
        assert suc


def test_enableRelay_2(qtbot):
    app.ui.relayDevice.setCurrentIndex(1)
    with mock.patch.object(app.app.relay,
                           'startCommunication',
                           return_value=None):
        suc = app.dispatch()
        assert suc


def test_enableRemote_1(qtbot):
    app.ui.remoteDevice.setCurrentIndex(0)
    with mock.patch.object(app.app.remote,
                           'startCommunication',
                           return_value=None):
        suc = app.dispatch()
        assert suc


def test_enableRemote_2(qtbot):
    app.ui.remoteDevice.setCurrentIndex(1)
    with mock.patch.object(app.app.remote,
                           'stopCommunication',
                           return_value=None):
        suc = app.dispatch()
        assert suc


def test_enableMeasure_1(qtbot):
    app.ui.measureDevice.setCurrentIndex(1)
    with mock.patch.object(app.app.measure,
                           'startCommunication',
                           return_value=None):
        suc = app.dispatch()
        assert suc


def test_enableMeasure_2(qtbot):
    app.ui.measureDevice.setCurrentIndex(0)
    with mock.patch.object(app.app.measure,
                           'stopCommunication',
                           return_value=None):
        suc = app.dispatch()
        assert suc


def test_sensorWeatherDispatch_1():
    app.ui.sensorWeatherDevice.setCurrentIndex(0)
    suc = app.dispatch()
    assert suc


def test_sensorWeatherDispatch_2():
    app.ui.sensorWeatherDevice.setCurrentIndex(1)
    suc = app.dispatch()
    assert suc


def test_skymeterDispatch_1():
    app.ui.skymeterDevice.setCurrentIndex(0)
    suc = app.dispatch()
    assert suc


def test_skymeterDispatch_2():
    app.ui.skymeterDevice.setCurrentIndex(1)
    suc = app.dispatch()
    assert suc


def test_powerDispatch_1():
    app.ui.powerDevice.setCurrentIndex(0)
    suc = app.dispatch()
    assert suc


def test_powerDispatch_2():
    app.ui.powerDevice.setCurrentIndex(1)
    suc = app.dispatch()
    assert suc


def test_astrometryDispatch_1():
    app.ui.astrometryDevice.setCurrentIndex(0)
    suc = app.dispatch()
    assert suc


def test_astrometryDispatch_2():
    app.ui.astrometryDevice.setCurrentIndex(1)
    suc = app.dispatch()
    assert suc
