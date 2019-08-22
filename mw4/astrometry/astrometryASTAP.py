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
import subprocess
import os
import shutil
import time
from collections import namedtuple
# external packages
from astropy.io import fits
import numpy as np
# local imports
from mw4.base import transform
from mw4.definitions import Solution, Solve


class AstrometryASTAP(object):
    """
    the class Astrometry inherits all information and handling of astrometry.net handling

    Keyword definitions could be found under
        https://fits.gsfc.nasa.gov/fits_dictionary.html

        >>> astrometry = AstrometryASTAP()

    """

    __all__ = ['AstrometryASTAP',
               'solveASTAP',
               'abortASTAP',
               ]

    version = '0.100.0'
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.result = (False, [])
        self.process = None

    @staticmethod
    def getWCSHeaderASTAP(wcsTextFile=None):
        """
        getWCSHeader reads the text file give by astap line by line and returns the values as
        part of a header part of a fits HDU header back.

        :param wcsTextFile: fits file with wcs data
        :return: wcsHeader
        """

        def removeKey(line):
            remove = ['SIMPLE', 'BITPIX', 'NAXIS', 'EXTEND', 'END']
            for key in remove:
                if line.startswith(key):
                    return True
            return False

        wcsHeader = fits.PrimaryHDU().header
        for line in wcsTextFile:
            if removeKey(line):
                continue
            if '=' in line:
                splitKeyValue = line.split('=')
                if len(splitKeyValue) != 2:
                    continue
                key, value = splitKeyValue
                # splitting inline comments and removing them
                splitValueComment = value.split('/')
                value = splitValueComment[0].strip()
                if len(splitValueComment) == 1:
                    comment = ''
                else:
                    comment = splitValueComment[1].strip()
            elif line.startswith('COMMENT'):
                key = 'COMMENT'
                value = line.strip('\n').strip().replace("'", '"')[8:]
                comment = ''
            else:
                key = line
                value = "''"
                comment = ''
            key = key.strip()
            if value.startswith("'"):
                value = value.strip("'").strip()
            else:
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except Exception:
                    value = str(value)
                finally:
                    pass
            if comment:
                wcsHeader.append((key, value, comment))
            else:
                wcsHeader.append((key, value))
        return wcsHeader

    def runASTAP(self, binPath='', tempPath='', fitsPath='', options='', timeout=30):
        """
        runSolveField solves finally the xy star list and writes the WCS data in a fits
        file format

        :param binPath:   full path to image2xy executable
        :param tempPath:  full path to star file
        :param fitsPath: full path to fits file in temp dir
        :param options: additional solver options e.g. ra and dec hint
        :param timeout:
        :return: success
        """

        runnable = [binPath,
                    '-f',
                    fitsPath,
                    '-o',
                    tempPath,
                    ]

        runnable += options

        timeStart = time.time()
        try:
            self.process = subprocess.Popen(args=runnable,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE
                                            )
            stdout, stderr = self.process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as e:
            self.logger.debug(e)
            return False
        except Exception as e:
            self.logger.error(f'error: {e} happened')
            return False
        else:
            delta = time.time() - timeStart
            self.logger.debug(f'astap took {delta}s return code: '
                              + str(self.process.returncode)
                              + ' stderr: '
                              + stderr.decode().replace('\n', ' ')
                              + ' stdout: '
                              + stdout.decode().replace('\n', ' ')
                              )

        success = (self.process.returncode == 0)

        return success

    def solveASTAP(self, app='', fitsPath='', raHint=None, decHint=None, scaleHint=None,
                   radius=2, timeout=30, updateFits=False):
        """
        Solve uses the astap solver capabilities. The intention is to use an
        offline solving capability, so we need a installed instance. As we go multi
        platform and we need to focus on MW function, we use the astap package
        which could be downloaded for all platforms. Many thanks to them providing such a
        nice package.

        :param app: which astrometry implementation to choose
        :param fitsPath:  full path to fits file
        :param raHint:  ra dest to look for solve in J2000
        :param decHint:  dec dest to look for solve in J2000
        :param scaleHint:  scale to look for solve in J2000
        :param radius:  search radius around target coordinates
        :param timeout: time after the subprocess will be killed.
        :param updateFits:  if true update Fits image file with wcsHeader data

        :return: success
        """

        self.process = None
        self.result = Solution(success=False,
                               solve=[])

        if not os.path.isfile(fitsPath):
            return False

        tempPath = self.tempDir + '/temp'
        wcsPath = self.tempDir + '/temp.wcs'
        if os.path.isfile(wcsPath):
            os.remove(wcsPath)

        binPathASTAP = self.solveApp[app]['programPath'] + '/astap'

        _, _, scaleFITS, raFITS, decFITS = self.readFitsData(fitsPath=fitsPath)

        # if parameters are passed, they have priority
        if raHint is None:
            raHint = raFITS
        if decHint is None:
            decHint = decFITS

        options = ['-ra',
                   f'{raHint}',
                   '-spd',
                   f'{decHint + 90}',
                   '-r',
                   f'{radius:1.1f}',
                   '-t',
                   '0.005',
                   ]

        suc = self.runASTAP(binPath=binPathASTAP,
                            fitsPath=fitsPath,
                            tempPath=tempPath,
                            options=options,
                            timeout=timeout,
                            )
        if not suc:
            self.logger.error(f'astap error in [{fitsPath}]')
            return False

        if not os.path.isfile(wcsPath):
            self.logger.error(f'solve files for [{wcsPath}] missing')
            return False

        with open(wcsPath) as wcsTextFile:
            wcsHeader = self.getWCSHeaderASTAP(wcsTextFile=wcsTextFile)

        with fits.open(fitsPath, mode='update') as fitsHDU:
            solve, header = self.getSolutionFromWCS(fitsHeader=fitsHDU[0].header,
                                                    wcsHeader=wcsHeader,
                                                    updateFits=updateFits)
            fitsHDU[0].header = header

        solve = Solve(raJ2000=solve.raJ2000,
                      decJ2000=solve.decJ2000,
                      angle=solve.angle,
                      scale=solve.scale,
                      error=solve.error,
                      flipped=solve.flipped,
                      path=fitsPath)
        self.result = Solution(success=True,
                               solve=solve)
        return True

    def abortASTAP(self):
        """
        abortNET stops the solving function hardly just by killing the process

        :return: success
        """

        if self.process:
            self.process.kill()
            return True
        else:
            return False
