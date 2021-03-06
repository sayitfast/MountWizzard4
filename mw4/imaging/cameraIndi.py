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
import logging
import zlib
import os
# external packages
import astropy.io.fits as fits
# local imports
from mw4.base.loggerMW import CustomLogger
from mw4.base.indiClass import IndiClass


class CameraIndi(IndiClass):
    """
    the class Camera inherits all information and handling of the Camera device.


        >>> c = CameraIndi(app=None, signals=None, data=None)
    """

    __all__ = ['CameraIndi',
               ]

    logger = logging.getLogger(__name__)
    log = CustomLogger(logger, {})

    # update rate to 1000 milli seconds for setting indi server
    UPDATE_RATE = 1000

    def __init__(self, app=None, signals=None, data=None):
        super().__init__(app=app, data=data)

        self.signals = signals
        self.data = data
        self.imagePath = ''

    def setUpdateConfig(self, deviceName):
        """
        _setUpdateRate corrects the update rate of camera devices to get an defined
        setting regardless, what is setup in server side.

        :param deviceName:
        :return: success
        """

        if deviceName != self.name:
            return False

        if self.device is None:
            return False

        # set BLOB mode also
        self.client.setBlobMode(blobHandling='Also',
                                deviceName=deviceName)
        # setting a object name
        objectName = self.device.getText('FITS_HEADER')
        objectName['FITS_OBJECT'] = 'skymodel'
        self.client.sendNewText(deviceName=deviceName,
                                propertyName='FITS_HEADER',
                                elements=objectName,
                                )
        # setting WCS Control off
        wcs = self.device.getSwitch('WCS_CONTROL')
        wcs['WCS_DISABLE'] = True
        self.client.sendNewSwitch(deviceName=deviceName,
                                  propertyName='WCS_CONTROL',
                                  elements=wcs,
                                  )
        # setting active device for telescope
        telescope = self.device.getText('ACTIVE_DEVICES')
        telescope['ACTIVE_TELESCOPE'] = 'LX200 10micron'
        self.client.sendNewText(deviceName=deviceName,
                                propertyName='ACTIVE_DEVICES',
                                elements=telescope,
                                )
        # setting polling updates in driver
        update = self.device.getNumber('POLLING_PERIOD')
        if 'PERIOD_MS' not in update:
            return False
        if update.get('PERIOD_MS', 0) == self.UPDATE_RATE:
            return True
        update['PERIOD_MS'] = self.UPDATE_RATE
        suc = self.client.sendNewNumber(deviceName=deviceName,
                                        propertyName='POLLING_PERIOD',
                                        elements=update,
                                        )

        return suc

    def setExposureState(self):
        """

        :return: success
        """

        if not hasattr(self.device, 'CCD_EXPOSURE'):
            return False

        value = self.data.get('CCD_EXPOSURE.CCD_EXPOSURE_VALUE', 0)

        if self.device.CCD_EXPOSURE['state'] == 'Idle':
            self.signals.message.emit('')
        elif self.device.CCD_EXPOSURE['state'] == 'Busy':
            if value == 0:
                self.signals.integrated.emit()
                self.signals.message.emit('download')
            else:
                self.signals.message.emit(f'expose {value:2.0f} s')
        elif self.device.CCD_EXPOSURE['state'] == 'Ok':
            self.signals.message.emit('')
        return True

    def updateNumber(self, deviceName, propertyName):
        """
        updateNumber is called whenever a new number is received in client. it runs
        through the device list and writes the number data to the according locations.

        :param deviceName:
        :param propertyName:
        :return:
        """
        if not super().updateNumber(deviceName, propertyName):
            return False

        if propertyName == 'CCD_EXPOSURE':
            self.setExposureState()

        return True

    def updateBLOB(self, deviceName, propertyName):
        """
        updateBLOB is called whenever a new BLOB is received in client. it runs
        through the device list and writes the number data to the according locations.

        :param deviceName:
        :param propertyName:
        :return: success
        """

        if not super().updateBLOB(deviceName, propertyName):
            return False

        data = self.device.getBlob(propertyName)

        if 'value' not in data:
            return False
        if 'name' not in data:
            return False
        if 'format' not in data:
            return False
        if data['name'] != 'CCD1':
            return False
        if not self.imagePath:
            return False
        if not os.path.isdir(os.path.dirname(self.imagePath)):
            return False

        if data['format'] == '.fits.fz':
            HDU = fits.HDUList.fromstring(data['value'])
            fits.writeto(self.imagePath, HDU[0].data, HDU[0].header, overwrite=True)
            self.log.warning('Image BLOB is in FPacked format')

        elif data['format'] == '.fits.z':
            HDU = fits.HDUList.fromstring(zlib.decompress(data['value']))
            fits.writeto(self.imagePath, HDU[0].data, HDU[0].header, overwrite=True)
            self.log.warning('Image BLOB is compressed fits format')

        elif data['format'] == '.fits':
            HDU = fits.HDUList.fromstring(data['value'])
            fits.writeto(self.imagePath, HDU[0].data, HDU[0].header, overwrite=True)
            self.log.warning('Image BLOB is uncompressed fits format')

        else:
            self.log.warning('Image BLOB is not supported')

        self.signals.saved.emit(self.imagePath)
        return True

    def sendDownloadMode(self, fastReadout=False):
        """
        setDownloadMode sets the readout speed of the camera

        :return: success
        """

        if not self.device:
            return False

        # setting fast mode:
        quality = self.device.getSwitch('READOUT_QUALITY')
        self.log.info(f'camera has readout quality entry: {quality}')
        quality['QUALITY_LOW'] = fastReadout
        quality['QUALITY_HIGH'] = not fastReadout
        suc = self.client.sendNewSwitch(deviceName=self.name,
                                        propertyName='READOUT_QUALITY',
                                        elements=quality,
                                        )

        return suc

    def expose(self,
               imagePath='',
               expTime=3,
               binning=1,
               fastReadout=True,
               posX=0,
               posY=0,
               width=1,
               height=1,
               ):
        """

        :param imagePath:
        :param expTime:
        :param binning:
        :param fastReadout:
        :param posX:
        :param posY:
        :param width:
        :param height:
        :return: success
        """

        if not self.device:
            return False

        self.imagePath = imagePath

        suc = self.sendDownloadMode(fastReadout=fastReadout)
        if not suc:
            self.log.info('Camera has no download quality settings')

        # setting binning value for x and y equally
        indiCmd = self.device.getNumber('CCD_BINNING')
        indiCmd['HOR_BIN'] = binning
        indiCmd['VER_BIN'] = binning
        suc = self.client.sendNewNumber(deviceName=self.name,
                                        propertyName='CCD_BINNING',
                                        elements=indiCmd,
                                        )
        if not suc:
            return False

        indiCmd = self.device.getNumber('CCD_FRAME')
        indiCmd['X'] = posX
        indiCmd['Y'] = posY
        indiCmd['WIDTH'] = width
        indiCmd['HEIGHT'] = height
        suc = self.client.sendNewNumber(deviceName=self.name,
                                        propertyName='CCD_FRAME',
                                        elements=indiCmd,
                                        )
        if not suc:
            return False

        # setting and starting exposure
        indiCmd = self.device.getNumber('CCD_EXPOSURE')
        indiCmd['CCD_EXPOSURE_VALUE'] = expTime
        suc = self.client.sendNewNumber(deviceName=self.name,
                                        propertyName='CCD_EXPOSURE',
                                        elements=indiCmd,
                                        )
        return suc

    def abort(self):
        """
        abort cancels the exposing

        :return: success
        """

        if not self.device:
            return False

        indiCmd = self.device.getSwitch('CCD_ABORT_EXPOSURE')

        if 'ABORT' not in indiCmd:
            return False

        indiCmd['ABORT'] = True
        suc = self.client.sendNewSwitch(deviceName=self.name,
                                        propertyName='CCD_ABORT_EXPOSURE',
                                        elements=indiCmd,
                                        )

        return suc

    def sendCoolerSwitch(self, coolerOn=False):
        """
        sendCoolerTemp send the desired cooler temp, but does not switch on / off the cooler

        :param coolerOn:
        :return: success
        """

        if not self.device:
            return False

        # setting fast mode:
        cooler = self.device.getSwitch('CCD_COOLER')

        if 'COOLER_ON' not in cooler:
            return False

        cooler['COOLER_ON'] = coolerOn
        cooler['COOLER_OFF'] = not coolerOn
        suc = self.client.sendNewSwitch(deviceName=self.name,
                                        propertyName='CCD_COOLER',
                                        elements=cooler,
                                        )

        return suc

    def sendCoolerTemp(self, temperature=0):
        """
        sendCoolerTemp send the desired cooler temp, indi does automatically start cooler

        :param temperature:
        :return: success
        """

        if not self.device:
            return False

        # setting fast mode:
        temp = self.device.getNumber('CCD_TEMPERATURE')

        if 'CCD_TEMPERATURE_VALUE' not in temp:
            return False

        temp['CCD_TEMPERATURE_VALUE'] = temperature
        suc = self.client.sendNewNumber(deviceName=self.name,
                                        propertyName='CCD_TEMPERATURE',
                                        elements=temp,
                                        )

        return suc
