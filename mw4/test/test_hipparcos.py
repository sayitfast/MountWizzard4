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
import pytest
import unittest.mock as mock
import PyQt5
# external packages
import skyfield.api
# local import
from mw4 import mainApp

from mw4.modeldata import hipparcos

test = PyQt5.QtWidgets.QApplication([])
mwGlob = {'workDir': '.',
          'configDir': './mw4/test/config',
          'dataDir': './mw4/test/config',
          'modeldata': 'test',
          }
app = mainApp.MountWizzard4(mwGlob=mwGlob)
topo = skyfield.toposlib.Topos(longitude_degrees=11,
                               latitude_degrees=48,
                               elevation_m=500)
app.mount.obsSite.location = topo
data = hipparcos.Hipparcos(app=app,
                           mwGlob=mwGlob)


def test_data_available():
    assert len(data.alignStars) > 0


def test_calculateAlignStarPositionsAltAz_1():
    star = dict()
    star['Achernar'] = [0.42636313743386084, -0.9989721040992605, 4.267359632399454e-07,
                        -1.9431237114262957e-07, 0.022680000001570513, 4.512483521476569e-05]
    data.alignStars = star

    data.calculateAlignStarPositionsAltAz()
    assert ['Achernar'] == data.name


def test_calculateAlignStarPositionsAltAz_2():
    star = dict()
    star['Achernar'] = [0.42636313743386084, -0.9989721040992605, 4.267359632399454e-07,
                        -1.9431237114262957e-07, 0.022680000001570513, 4.512483521476569e-05]
    star['Acrux'] = [3.257647500944081, -1.1012877251083137, -1.7147915360582993e-07,
                     -7.141291885025191e-08, 0.010169999999992536, 0.00018371089505169385]
    data.alignStars = star

    data.calculateAlignStarPositionsAltAz()
    assert ['Achernar', 'Acrux'] == data.name


def test_getAlignStarRaDecFromIndex_1():
    star = dict()
    star['Achernar'] = [0.42636313743386084, -0.9989721040992605, 4.267359632399454e-07,
                        -1.9431237114262957e-07, 0.022680000001570513, 4.512483521476569e-05]
    star['Acrux'] = [3.257647500944081, -1.1012877251083137, -1.7147915360582993e-07,
                     -7.141291885025191e-08, 0.010169999999992536, 0.00018371089505169385]
    data.alignStars = star
    ra, dec = data.getAlignStarRaDecFromIndex('Achernar')
    assert ra is not None
    assert dec is not None


def test_getAlignStarRaDecFromIndex_2():
    star = dict()
    star['Achernar'] = [0.42636313743386084, -0.9989721040992605, 4.267359632399454e-07,
                        -1.9431237114262957e-07, 0.022680000001570513, 4.512483521476569e-05]
    star['Acrux'] = [3.257647500944081, -1.1012877251083137, -1.7147915360582993e-07,
                     -7.141291885025191e-08, 0.010169999999992536, 0.00018371089505169385]
    data.alignStars = star
    ra, dec = data.getAlignStarRaDecFromIndex('Test')
    assert ra is None
    assert dec is None
