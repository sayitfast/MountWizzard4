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
# Python  v3.7.4
#
# Michael Würtenberger
# (c) 2019
#
# Licence APL2.0
#
###########################################################
# standard libraries
# external packages
import PyQt5
import numpy as np
# local import


class SettImaging(object):
    """
    """

    def __init__(self):
        # updating gui regular
        self.app.update1s.connect(self.updateParameters)

        # update when driver changes items
        self.app.cover.client.signals.newSwitch.connect(self.updateCoverStatGui)
        self.app.cover.client.signals.newText.connect(self.updateCoverStatGui)
        self.app.cover.client.signals.newNumber.connect(self.updateCoverStatGui)

        # gui actions
        self.ui.coverPark.clicked.connect(self.setCoverPark)
        self.ui.coverUnpark.clicked.connect(self.setCoverUnpark)
        self.ui.checkFastDownload.clicked.connect(self.setDownloadMode)
        self.clickable(self.ui.coolerTemp).connect(self.setCoolerTemp)

    def initConfig(self):
        """

        :return:
        """

        config = self.app.config['mainW']
        self.ui.expTime.setValue(config.get('expTime', 1))
        self.ui.binning.setValue(config.get('binning', 1))
        self.ui.subFrame.setValue(config.get('subFrame', 100))
        self.ui.subFrame.setValue(config.get('subFrame', 100))
        self.ui.subFrame.setValue(config.get('subFrame', 100))
        self.ui.checkFastDownload.setChecked(config.get('checkFastDownload', False))
        self.ui.checkKeepImages.setChecked(config.get('checkKeepImages', False))
        self.ui.searchRadius.setValue(config.get('searchRadius', 2))
        self.ui.solveTimeout.setValue(config.get('solveTimeout', 30))

        return True

    def storeConfig(self):
        """

        :return:
        """

        config = self.app.config['mainW']
        config['expTime'] = self.ui.expTime.value()
        config['binning'] = self.ui.binning.value()
        config['subFrame'] = self.ui.subFrame.value()
        config['searchRadius'] = self.ui.searchRadius.value()
        config['solveTimeout'] = self.ui.solveTimeout.value()
        config['checkFastDownload'] = self.ui.checkFastDownload.isChecked()
        config['checkKeepImages'] = self.ui.checkKeepImages.isChecked()
        config['settleTimeMount'] = self.ui.settleTimeMount.value()
        config['settleTimeDome'] = self.ui.settleTimeDome.value()

        return True

    def updateParameters(self):
        """

        :return: success
        """

        focalLength = self.app.telescope.focalLength
        aperture = self.app.telescope.aperture
        pixelSizeX = self.app.imaging.pixelSizeX
        pixelSizeY = self.app.imaging.pixelSizeY
        pixelX = self.app.imaging.pixelX
        pixelY = self.app.imaging.pixelY
        filterNumber = self.app.imaging.filterNumber
        filterNames = self.app.imaging.filterNames
        coolerTemp = self.app.imaging.coolerTemp
        coolerPower = self.app.imaging.coolerPower

        self.ui.pixelSizeX.setText(f'{pixelSizeX:2.2f}')
        self.ui.pixelSizeY.setText(f'{pixelSizeY:2.2f}')
        self.ui.pixelX.setText(f'{pixelX:5.0f}')
        self.ui.pixelY.setText(f'{pixelY:5.0f}')
        self.ui.filterNumber.setText(f'{filterNumber:1.0f}')
        self.ui.coolerTemp.setText(f'{coolerTemp:3.1f}')
        self.ui.coolerPower.setText(f'{coolerPower:3.1f}')

        if not filterNames:
            return False
        key = f'FILTER_SLOT_NAME_{filterNumber:1.0f}'
        text = filterNames.get(key, 'not found')
        self.ui.filterText.setText(f'{text}')

        if focalLength and pixelSizeX and pixelSizeY:
            resolutionX = pixelSizeX / focalLength * 206.265
            resolutionY = pixelSizeY / focalLength * 206.265
            self.app.mainW.ui.resolutionX.setText(f'{resolutionX:2.2f}')
            self.app.mainW.ui.resolutionY.setText(f'{resolutionY:2.2f}')

        if focalLength and aperture:
            speed = focalLength / aperture
            self.app.mainW.ui.speed.setText(f'{speed:2.1f}')

        if aperture:
            dawes = 116 / aperture
            rayleigh = 138 / aperture
            magLimit = 7.7 + (5 * np.log10(aperture / 10))
            self.app.mainW.ui.dawes.setText(f'{dawes:2.2f}')
            self.app.mainW.ui.rayleigh.setText(f'{rayleigh:2.2f}')
            self.app.mainW.ui.magLimit.setText(f'{magLimit:2.2f}')

        if pixelSizeX and pixelSizeY and pixelX and pixelY and focalLength:
            FOVX = pixelSizeX / focalLength * 206.265 * pixelX / 3600
            FOVY = pixelSizeY / focalLength * 206.265 * pixelY / 3600
            self.app.mainW.ui.FOVX.setText(f'{FOVX:2.2f}')
            self.app.mainW.ui.FOVY.setText(f'{FOVY:2.2f}')

    def updateCoverStatGui(self):
        """
        updateCoverStatGui changes the style of the button related to the state of the FliFlat

        :return: success for test
        """

        value = self.app.cover.data.get('Cover', '-').strip().upper()
        if value == 'OPEN':
            self.changeStyleDynamic(self.ui.coverUnpark, 'running', True)
        elif value == 'CLOSED':
            self.changeStyleDynamic(self.ui.coverPark, 'running', True)
        else:
            self.changeStyleDynamic(self.ui.coverPark, 'running', False)
            self.changeStyleDynamic(self.ui.coverUnpark, 'running', False)

        value = self.app.cover.data.get('Cover', '-')
        self.ui.coverStatusText.setText(value)

        value = self.app.cover.data.get('Motor', '-')
        self.ui.coverMotorText.setText(value)

    def setCoverPark(self):
        """

        :return: success
        """

        self.app.cover.sendCoverPark(park=True)
        return True

    def setCoverUnpark(self):
        """

        :return: success
        """

        self.app.cover.sendCoverPark(park=False)
        return True

    def setCoolerTemp(self):
        """

        :return: true for test purpose
        """

        msg = PyQt5.QtWidgets.QMessageBox
        actValue = self.app.imaging.coolerTemp
        if actValue is None:
            msg.critical(self,
                         'Error Message',
                         'Value cannot be set when not connected !')
            return False
        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getInt(self,
                               'Set cooler temperature',
                               'Value (-20..+20):',
                               actValue,
                               -20,
                               20,
                               1,
                               )

        if not ok:
            return False

        self.app.imaging.sendCoolerTemp(temperature=value)

        return True

    def setDownloadMode(self):
        """

        :return:
        """

        mode = self.ui.checkFastDownload.isChecked()
        self.app.imaging.setDownloadMode(fastReadout=mode)

        return True
