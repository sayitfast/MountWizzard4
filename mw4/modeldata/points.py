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
import logging
import os
import json
# external packages
import numpy as np
# local imports

__all__ = ['HaDecToAltAz',
           ]

version = '0.1'


def HaDecToAltAz(ha, dec, lat):
    """
    HaDecToAltAz is derived from http://www.stargazing.net/kepler/altaz.html

    :param ha:
    :param dec:
    :param lat:
    :return:
    """

    ha = (ha * 360 / 24 + 360.0) % 360.0
    dec = np.radians(dec)
    ha = np.radians(ha)
    lat = np.radians(lat)
    alt = np.arcsin(np.sin(dec) * np.sin(lat) + np.cos(dec) * np.cos(lat) * np.cos(ha))
    value = (np.sin(dec) - np.sin(alt) * np.sin(lat)) / (np.cos(alt) * np.cos(lat))
    value = np.clip(value, -1.0, 1.0)
    A = np.arccos(value)
    if np.sin(ha) >= 0.0:
        az = 2 * np.pi - A
    else:
        az = A
    az = np.degrees(az)
    alt = np.degrees(alt)
    return alt, az


class DataPoint(object):
    """
    The class Data inherits all information and handling of modeldata data and other
    attributes. this includes horizon data, model points data and their persistence

        >>> data = DataPoint(
        >>>                  mwGlob=mwglob,
        >>>                  location=None,
        >>>                  )
    """

    __all__ = ['DataPoint',
               'genGreaterCircle',
               'genGrid',
               'genInitial',
               'loadBuildP',
               'saveBuildP',
               'clearPoints'
               'loadHorizonP',
               'saveHorizonP',
               'clearHorizonP',
               'generateCelestialEquator',
               'hip',
               ]
    version = '0.1'
    logger = logging.getLogger(__name__)

    # data for generating greater circles, dec and step only for east, west is reversed
    DEC = {'min': [-15, 0, 15, 30, 45, 60, 75],
           'norm': [-15, 0, 15, 30, 45, 60, 75],
           'med': [-15, -5, 5, 15, 25, 40, 55, 70, 85],
           'max': [-15, -5, 5, 15, 25, 35, 45, 55, 65, 75, 85],
           }
    STEP = {'min': [15, -15, 15, -15, 15, -30, 30],
            'norm': [10, -10, 10, -10, 10, -20, 20],
            'med': [10, -10, 10, -10, 10, -10, 10, -30, 30],
            'max': [10, -10, 10, -10, 10, -10, 10, -10, 10, -30, 30],
            }
    START = {'min': [-120, -5, -120, -5, -120, -5, -120,
                     5, 120, 5, 120, 5, 120, 5],
             'norm': [-120, -5, -120, -5, -120, -5, -120,
                      5, 120, 5, 120, 5, 120, 5],
             'med': [-120, -5, -120, -5, -120, -5, -120, -5, -120,
                     5, 120, 5, 120, 5, 120, 5, 120, 5],
             'max': [-120, -5, -120, -5, -120, -5, -120, -5, -120, -5, -120,
                     5, 120, 5, 120, 5, 120, 5, 120, 5, 120, 5],
             }
    STOP = {'min': [0, -120, 0, -120, 0, -120, 0,
                    120, 0, 120, 0, 120, 0, 120],
            'norm': [0, -120, 0, -120, 0, -120, 0,
                     120, 0, 120, 0, 120, 0, 120],
            'med': [0, -120, 0, -120, 0, -120, 0, -120, 0,
                    120, 0, 120, 0, 120, 0, 120, 0, 120, 0],
            'max': [0, -120, 0, -120, 0, -120, 0, -120, 0, -120, 0,
                    120, 0, 120, 0, 120, 0, 120, 0, 120, 0, 120, 0],
            }

    def __init__(self,
                 location=None,
                 mwGlob=None,
                 ):

        self.mwGlob = mwGlob
        self.lat = location.latitude.degrees
        self._horizonPFile = None
        self._buildPFile = None
        self._horizonP = [(0, 0), (0, 360)]
        self._buildP = list()

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = value

    @property
    def horizonPFile(self):
        return self._horizonPFile

    @horizonPFile.setter
    def horizonPFile(self, value):
        self._horizonPFile = value

    @property
    def buildPFile(self):
        return self._buildPFile

    @buildPFile.setter
    def buildPFile(self, value):
        self._buildPFile = value

    @property
    def buildP(self):
        return self._buildP

    @buildP.setter
    def buildP(self, value):
        if not isinstance(value, list):
            self._buildP = list()
            return
        if not all([isinstance(x, tuple) for x in value]):
            self.logger.error('malformed value: {0}'.format(value))
            self._buildP = list()
            return
        self._buildP = value

    def addBuildP(self, value=None, position=None):
        """
        addBuildP extends the list of modeldata points. the new point could be added at the end
        of the list (default) or in any location in the list.

        :param value:
        :param position:
        :return:
        """

        if value is None:
            return False
        if not isinstance(value, tuple):
            self.logger.error('malformed value: {0}'.format(value))
            return False
        if len(value) != 2:
            self.logger.error('malformed value: {0}'.format(value))
            return False
        if position is None:
            position = len(self._buildP)
        if not isinstance(position, (int, float)):
            self.logger.error('malformed position: {0}'.format(position))
            return False
        position = int(position)
        position = min(len(self._buildP), position)
        position = max(0, position)
        self._buildP.insert(position, value)
        return True

    def delBuildP(self, position):
        """
        delBuildP deletes one point from the modeldata points list at the given index.

        :param position:
        :return:
        """

        if not isinstance(position, (int, float)):
            self.logger.error('malformed position: {0}'.format(position))
            return False
        position = int(position)
        if position < 0 or position > len(self._buildP) - 1:
            self.logger.error('invalid position: {0}'.format(position))
            return False
        self._buildP.pop(position)
        return True

    def clearBuildP(self):
        self._buildP = list()

    def checkHorizonBoundaries(self):
        if self._horizonP[0] != (0, 0):
            self._horizonP.insert(0, (0, 0))
        horMax = len(self._horizonP)
        if self._horizonP[horMax - 1] != (0, 360):
            self._horizonP.insert(horMax, (0, 360))

    @property
    def horizonP(self):
        self._horizonP = sorted(self._horizonP, key=lambda x: x[1])
        self.checkHorizonBoundaries()
        return self._horizonP

    @horizonP.setter
    def horizonP(self, value):
        if not isinstance(value, list):
            self.clearHorizonP()
            return
        if not all([isinstance(x, tuple) for x in value]):
            self.logger.error('malformed value: {0}'.format(value))
            self.clearHorizonP()
            return
        self._horizonP = value
        self.checkHorizonBoundaries()

    @staticmethod
    def checkFormat(value):
        if not isinstance(value, list):
            return False
        if not all([isinstance(x, list) for x in value]):
            return False
        if not all([len(x) == 2 for x in value]):
            return False
        return True

    def addHorizonP(self, value=None, position=None):
        """
        addHorizonP extends the list of modeldata points. the new point could be added at the
        end of the list (default) or in any location in the list.

        :param value:
        :param position:
        :return:
        """

        if value is None:
            return False
        if not isinstance(value, tuple):
            self.logger.error('malformed value: {0}'.format(value))
            return False
        if len(value) != 2:
            self.logger.error('malformed value: {0}'.format(value))
            return False
        if position is None:
            position = len(self._horizonP)
        if not isinstance(position, (int, float)):
            self.logger.error('malformed position: {0}'.format(position))
            return False
        position = int(position)
        position = min(len(self._horizonP), position)
        position = max(0, position)
        self._horizonP.insert(position, value)
        return True

    def delHorizonP(self, position):
        """
        delHorizonP deletes one point from the modeldata points list at the given index.

        :param position:
        :return:
        """

        if not isinstance(position, (int, float)):
            self.logger.error('malformed position: {0}'.format(position))
            return False
        position = int(position)
        if position < 0 or position > len(self._horizonP) - 1:
            self.logger.error('invalid position: {0}'.format(position))
            return False
        if self._horizonP[position] == (0, 0):
            return False
        if self._horizonP[position] == (0, 360):
            return False
        self._horizonP.pop(position)
        return True

    def clearHorizonP(self):
        self._horizonP = [(0, 0), (0, 360)]

    def isAboveHorizon(self, point):
        """
        isAboveHorizon calculates for a given point the relationship to the actual horizon
        and determines if this point is above the horizon line. for that there will be a
        linear interpolation for the horizon line points.

        :param point:
        :return:
        """

        if point[1] > 360:
            point = (point[0], 360)
        if point[1] < 0:
            point = (point[0], 0)
        x = range(0, 361)
        y = np.interp(x,
                      [i[1] for i in self._horizonP],
                      [i[0] for i in self._horizonP],
                      )
        if point[0] > y[int(point[1])]:
            return True
        else:
            return False

    def deleteBelowHorizon(self):
        self._buildP = [x for x in self._buildP if self.isAboveHorizon(x)]

    def loadBuildP(self, fileName=None):
        """
        loadBuildP loads a modeldata pints file and stores the data in the buildP list.
        necessary conversion are made.

        :param fileName: name of file to be handled
        :return: success
        """

        if fileName is None:
            if not self._buildPFile:
                return False
            fileName = self.mwGlob['configDir'] + '/' + self._buildPFile + '.bpts'
        if not os.path.isfile(fileName):
            return False

        try:
            with open(fileName, 'r') as handle:
                value = json.load(handle)
        except Exception as e:
            self.logger.error('Cannot load: {0}, error: {1}'.format(fileName, e))
            return False

        suc = self.checkFormat(value)
        if not suc:
            self.clearBuildP()
            return False
        # json makes list out of tuple, was to be reversed
        value = [tuple(x) for x in value]
        self._buildP = value
        self._buildPFile = os.path.basename(fileName).split('.')[0]
        return True

    def saveBuildP(self, fileName=None):
        """
        saveBuildP saves the actual modeldata points list in a file in json dump format

        :param fileName: name of file to be handled
        :return: success
        """

        if fileName is None:
            if not self._buildPFile:
                return False
            fileName = self.mwGlob['configDir'] + '/' + self._buildPFile + '.bpts'

        with open(fileName, 'w') as handle:
            json.dump(self._buildP,
                      handle,
                      indent=4)
        return True

    def loadHorizonP(self, fileName=None):
        """
        loadHorizonP loads a modeldata pints file and stores the data in the buildP list.
        necessary conversion are made.

        :param fileName: name of file to be handled
        :return: success
        """

        if fileName is None:
            if not self._horizonPFile:
                return False
            fileName = self.mwGlob['configDir'] + '/' + self._horizonPFile + '.hpts'
        if not os.path.isfile(fileName):
            return False

        try:
            with open(fileName, 'r') as handle:
                value = json.load(handle)
        except Exception as e:
            self.logger.error('Cannot load: {0}, error: {1}'.format(fileName, e))
            return False

        suc = self.checkFormat(value)
        if not suc:
            self.clearHorizonP()
            return False
        # json makes list out of tuple, was to be reversed
        value = [tuple(x) for x in value]
        self._horizonP = value
        self._horizonPFile = os.path.basename(fileName).split('.')[0]
        return True

    @staticmethod
    def checkBoundaries(points):
        """
        checkBoundaries removes point 0,0 and 0, 360 if present.

        :param points:
        :return: points
        """

        if points[0] == (0, 0):
            del points[0]
        if points[len(points) - 1] == (0, 360):
            del points[-1]
        return points

    def saveHorizonP(self, fileName=None):
        """
        saveHorizonP saves the actual modeldata points list in a file in json dump format

        :param fileName: name of file to be handled
        :return: success
        """

        if fileName is None:
            if not self._horizonPFile:
                return False
            fileName = self.mwGlob['configDir'] + '/' + self._horizonPFile + '.hpts'
        points = self.checkBoundaries(self.horizonP)
        with open(fileName, 'w') as handle:
            json.dump(points,
                      handle,
                      indent=4)
        return True

    def genHaDecParams(self, selection):
        """
        genHaDecParams selects the parameters for generating the boundaries for next
        step processing greater circles. the parameters are sorted for different targets
        actually for minimum slew distance between the points. defined is only the east
        side of data, the west side will be mirrored to the east one.

        :param selection: type of model we would like to use
        :return: yield tuple of dec value and step, start and stop for range
        """

        if selection not in self.DEC or selection not in self.STEP:
            return
        eastDec = self.DEC[selection]
        westDec = list(reversed(eastDec))
        decL = eastDec + westDec

        eastStepL = self.STEP[selection]
        westStepL = list(reversed(eastStepL))
        stepL = eastStepL + westStepL
        startL = self.START[selection]
        stopL = self.STOP[selection]

        for dec, step, start, stop in zip(decL, stepL, startL, stopL):
            yield dec, step, start, stop

    def genGreaterCircle(self, selection='norm'):
        """
        genGreaterCircle takes the generated boundaries for the rang routine and
        transforms ha, dec to alt az. reasonable values for the alt az values
        are 5 to 85 degrees.

        :param selection:
        :return: yields alt, az tuples which are above horizon
        """

        self.clearBuildP()
        for dec, step, start, stop in self.genHaDecParams(selection):
            for ha in range(start, stop, step):
                alt, az = HaDecToAltAz(ha / 10, dec, self.lat)
                # only values with above horizon = 0

                if 5 <= alt <= 85 and 2 < az < 358:
                    self.addBuildP((alt, az))
        return True

    @staticmethod
    def genGridGenerator(eastAlt, westAlt, minAz, stepAz, maxAz):
        """
        genGridGenerator generates the point values out of the given ranges of altitude
        and azimuth

        :param eastAlt:
        :param westAlt:
        :param minAz:
        :param stepAz:
        :param maxAz:
        :return:
        """

        for i, alt in enumerate(eastAlt):
            if i % 2:
                for az in range(minAz, 180, stepAz):
                    yield(alt, az)
            else:
                for az in range(180 - minAz, 0, -stepAz):
                    yield(alt, az)
        for i, alt in enumerate(westAlt):
            if i % 2:
                for az in range(180 + minAz, 360, stepAz):
                    yield(alt, az)
            else:
                for az in range(maxAz, 180, -stepAz):
                    yield(alt, az)

    def genGrid(self, minAlt=5, maxAlt=85, numbRows=5, numbCols=6):
        """
        genGrid generates a grid of points and transforms ha, dec to alt az. with given
        limits in alt, the min and max will be used as a hard condition. on az there is
        not given limit, therefore a split over the whole space (omitting the meridian)
        is done. the simplest way to avoid hitting the meridian is to enforce the number
        of cols to be a factor of 2. reasonable values for the grid are 5 to 85 degrees.
        defined is only the east side of data, the west side will be mirrored to the
        east one.
            the number of rows is 2 < x < 8
            the number of columns is 2 < x < 15

        :param minAlt: altitude min
        :param maxAlt: altitude max
        :param numbRows: numbRows
        :param numbCols: numbCols
        :return: yields alt, az tuples which are above horizon
        """

        if not 5 <= minAlt <= 85:
            return False
        if not 5 <= maxAlt <= 85:
            return False
        if not maxAlt > minAlt:
            return False
        if not 1 < numbRows < 9:
            return False
        if not 1 < numbCols < 16:
            return False
        if numbCols % 2:
            return False

        minAlt = int(minAlt)
        maxAlt = int(maxAlt)
        numbCols = int(numbCols)
        numbRows = int(numbRows)

        stepAlt = int((maxAlt - minAlt) / (numbRows - 1))
        eastAlt = list(range(minAlt, maxAlt + 1, stepAlt))
        westAlt = list(reversed(eastAlt))

        stepAz = int(360 / numbCols)
        minAz = int(180 / numbCols)
        maxAz = 360 - minAz

        self.clearBuildP()
        for point in self.genGridGenerator(eastAlt, westAlt, minAz, stepAz, maxAz):
            self.addBuildP(point)
        return True

    def genInitial(self, alt=30, azStart=10, numb=3):
        """
        genInitial generates a number of initial points for the first step of modeling

        :param alt:
        :param azStart:
        :param numb:
        :return: yields alt, az tuples which are above horizon
        """

        if not 5 <= alt <= 85:
            return False
        if not 2 < numb < 10:
            return False
        if not 0 <= azStart < 360:
            return False

        stepAz = int(360 / numb)

        self.clearBuildP()
        for az in range(azStart, 720, stepAz):
            self.addBuildP((alt, az % 360))
        return True

    def generateCelestialEquator(self):
        """
        generateCelestialEquator calculates a line for greater circles like a celestial
        equator for showing the paths in the hemisphere window.

        :return: celestial equator
        """

        celestialEquator = list()
        for dec in range(-15, 90, 15):
            for ha in range(- 119, 120, 3):
                az, alt = HaDecToAltAz(ha / 10, dec, self.lat)
                if alt > 0:
                    celestialEquator.append((az, alt))
        return celestialEquator