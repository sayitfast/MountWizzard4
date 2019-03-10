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
# external packages
import PyQt5.QtCore
import PyQt5.QtWidgets
import PyQt5.uic
# local import


class SettDevice(object):
    """
    the main window class handles the main menu as well as the show and no show part of
    any other window. all necessary processing for functions of that gui will be linked
    to this class. therefore window classes will have a threadpool for managing async
    processing if needed.
    """

    def __init__(self):
        self.deviceDropDowns = [self.ui.ccdDevice,
                                self.ui.astrometryDevice,
                                self.ui.domeDevice,
                                self.ui.environDevice,
                                self.ui.skymeterDevice,
                                self.ui.powerDevice,
                                self.ui.relayDevice,
                                self.ui.measureDevice,
                                self.ui.remoteDevice,
                                ]
        self.deviceDropDownKeys = ['ccdDevice',
                                   'astrometryDevice',
                                   'domeDevice',
                                   'environmentDevice',
                                   'skymeterDevice',
                                   'powerDevice',
                                   'relayDevice',
                                   'measureDevice',
                                   'remoteDevice',
                                   ]
        self.setupDeviceGui()
        self.ui.relayDevice.activated.connect(self.enableRelay)
        self.ui.remoteDevice.activated.connect(self.enableRemote)
        self.ui.measureDevice.activated.connect(self.enableMeasure)
        self.ui.environDevice.activated.connect(self.environDispatch)
        self.ui.skymeterDevice.activated.connect(self.skymaterDispatch)

    def initConfig(self):
        config = self.app.config['mainW']
        for dropDown, key in zip(self.deviceDropDowns, self.deviceDropDownKeys):
            dropDown.setCurrentIndex(config.get(key, 0))

        self.enableRelay()
        self.enableRemote()
        self.enableMeasure()
        self.environDispatch()
        return True

    def storeConfig(self):
        config = self.app.config['mainW']
        for dropDown, key in zip(self.deviceDropDowns, self.deviceDropDownKeys):
            config[key] = dropDown.currentIndex()

        return True

    def setupIcons(self):
        """
        setupIcons add icon from standard library to certain buttons for improving the
        gui of the app.

        :return:    True if success for test
        """
        return True

    def clearGUI(self):
        """
        clearGUI rewrites the gui in case of a special event needed for clearing up

        :return: success for test
        """
        return True

    def setupDeviceGui(self):
        """
        setupRelayGui handles the dropdown lists for all devices possible in mountwizzard.
        therefore we add the necessary entries to populate the list.

        :return: success for test
        """

        for dropDown in self.deviceDropDowns:
            dropDown.clear()
            dropDown.setView(PyQt5.QtWidgets.QListView())
            dropDown.addItem('No device selected')

        # adding special items
        self.ui.measureDevice.addItem('Built-In Measurement')
        self.ui.remoteDevice.addItem('Built-In Remote')
        self.ui.relayDevice.addItem('Built-In Relay KMTronic')
        self.ui.environDevice.addItem('Indi Driver')

        return True

    def enableRelay(self):
        """
        enableRelay allows to run the relay box.

        :return: success for test
        """

        # get index for relay tab
        tabWidget = self.ui.mainTabWidget.findChild(PyQt5.QtWidgets.QWidget, 'Relay')
        tabIndex = self.ui.mainTabWidget.indexOf(tabWidget)

        if self.ui.relayDevice.currentIndex() == 1:
            self.ui.mainTabWidget.setTabEnabled(tabIndex, True)
            self.ui.mainTabWidget.setStyleSheet(self.getStyle())
            self.app.message.emit('Relay enabled', 0)
            self.app.relay.startTimers()
            self.ui.relayDevice.setStyleSheet(self.BACK_GREEN)
        else:
            self.ui.mainTabWidget.setTabEnabled(tabIndex, False)
            self.ui.mainTabWidget.setStyleSheet(self.getStyle())
            self.app.message.emit('Relay disabled', 0)
            self.app.relay.stopTimers()
            self.ui.relayDevice.setStyleSheet(self.BACK_NORM)

        # update the style for showing the Relay tab
        self.ui.mainTabWidget.style().unpolish(self.ui.mainTabWidget)
        self.ui.mainTabWidget.style().polish(self.ui.mainTabWidget)
        return True

    def enableRemote(self):
        """
        remoteAccess enables or disables the remote access

        :return: true for test purpose
        """

        if self.ui.remoteDevice.currentIndex() == 1:
            self.app.remote.startRemote()
            self.app.message.emit('Remote enabled', 0)
            self.ui.remoteDevice.setStyleSheet(self.BACK_GREEN)
        else:
            self.app.remote.stopRemote()
            self.app.message.emit('Remote disabled', 0)
            self.ui.remoteDevice.setStyleSheet(self.BACK_NORM)

        return True

    def enableMeasure(self):
        """
        enableMeasure enables or disables the on board measurement process

        :return: true for test purpose
        """

        if self.ui.measureDevice.currentIndex() == 1:
            self.app.measure.startMeasurement()
            self.app.message.emit('Measurement enabled', 0)
            self.ui.measureDevice.setStyleSheet(self.BACK_GREEN)
        else:
            self.app.measure.stopMeasurement()
            self.app.message.emit('Measurement disabled', 0)
            self.ui.measureDevice.setStyleSheet(self.BACK_NORM)

        return True

    def environDispatch(self):
        """
        environDispatch selects the type of device for environment measures and start / stop
        them.
        in addition this function enables and disables other gui functions, which rely on
        the presence of a running driver

        :return: true for test purpose
        """

        self.ui.environGroup.setEnabled(False)
        self.ui.refractionGroup.setEnabled(False)
        self.ui.setRefractionManual.setEnabled(False)
        index = self.ui.environDevice.currentIndex()
        if index == 1:
            host = (self.ui.environHost.text(), int(self.ui.environPort.text()))
            self.app.environ.client.host = host
            self.app.environ.name = self.ui.environName.text()
            self.app.environ.startCommunication()
            # gui element to be used
            self.changeStyleDynamic(self.ui.environConnected, 'color', 'red')
        else:
            self.app.environ.stopCommunication()
            # gui elements not anymore to be used
            self.changeStyleDynamic(self.ui.environConnected, 'color', 'gray')

        return True

    def skymeterDispatch(self):
        """
        skymeterDispatch selects the type of device for environment measures and start / stop
        them.

        :return: true for test purpose
        """

        self.ui.skymeterGroup.setEnabled(False)
        index = self.ui.skymeterDevice.currentIndex()
        if index == 1:
            host = (self.ui.skymeter.text(), int(self.ui.skymeter.text()))
            self.app.skymeter.client.host = host
            self.app.skymeter.name = self.ui.environName.text()
            self.app.skymeter.startCommunication()
        else:
            self.app.skymeter.stopCommunication()

        return True
