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
import logging
from datetime import datetime
# external packages
import numpy as np
# local imports
from mw4.base import indiClass


class Telescope(indiClass.IndiClass):
    """
    the class SnoopTelescope inherits all information and handling of the Skymeter device

        >>>  Telescope(
        >>>                  host=host
        >>>                  name=''
        >>>                 )
    """

    __all__ = ['Telescope',
               ]

    version = '0.100.0'
    logger = logging.getLogger(__name__)

    # update rate to 10 seconds for setting indi server
    UPDATE_RATE = 10

    def __init__(self,
                 host=None,
                 name='',
                 ):
        super().__init__(host=host,
                         name=name
                         )
        self.focalLength = 0
        self.aperture = 0

    def setUpdateConfig(self, deviceName):
        """
        _setUpdateRate corrects the update rate of weather devices to get an defined
        setting regardless, what is setup in server side.

        :param deviceName:
        :return: success
        """

        if deviceName != self.name:
            return False

        if self.device is None:
            return False

        # reset basic data when started
        self.focalLength = 0
        self.aperture = 0

        update = self.device.getNumber('PERIOD_MS')

        if 'PERIOD' not in update:
            return False

        if update.get('PERIOD', 0) == self.UPDATE_RATE:
            return True

        update['PERIOD'] = self.UPDATE_RATE
        suc = self.client.sendNewNumber(deviceName=deviceName,
                                        propertyName='PERIOD_MS',
                                        elements=update)
        return suc

    def setParametersNumber(self, propertyName='', element='', value=0):
        """

        :param propertyName:
        :param element:
        :param value:
        :return: success
        """

        if propertyName == 'TELESCOPE_INFO':
            if element == 'TELESCOPE_APERTURE':
                print('telescope', value)
                self.aperture = value
            if element == 'TELESCOPE_FOCAL_LENGTH':
                print('telescope', value)
                self.focalLength = value
            return True
        return False

    def updateNumber(self, deviceName, propertyName):
        """
        updateNumber is called whenever a new number is received in client. it runs
        through the device list and writes the number data to the according locations.

        :param deviceName:
        :param propertyName:
        :return:
        """

        if self.device is None:
            return False
        if deviceName != self.name:
            return False

        if self.device is None:
            return False
        if deviceName != self.name:
            return False

        for element, value in self.device.getNumber(propertyName).items():
            key = propertyName + '.' + element
            self.data[key] = value
            # print(propertyName, element, value)

            self.setParametersNumber(propertyName=propertyName, element=element, value=value)

        return True
