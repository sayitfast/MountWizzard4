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
import subprocess
import os
import glob
import platform
# external packages
import PyQt5.QtWidgets
from skyfield.api import Angle
from astropy.io import fits
from astropy.wcs import WCS
import astropy.wcs
from PyQt5.QtTest import QTest
import numpy as np
# local imports
from mw4.base import tpool


class AstrometrySignals(PyQt5.QtCore.QObject):
    """
    The AstrometrySignals class offers a list of signals to be used and instantiated by the
    Worker class to get signals for error, finished and result to be transferred to the
    caller back
    """

    __all__ = ['AstrometrySignals']
    version = '0.1'

    solveDone = PyQt5.QtCore.pyqtSignal()
    solveResult = PyQt5.QtCore.pyqtSignal(object)


class AstrometryKstars(object):
    """
    the class Astrometry inherits all information and handling of astrometry.net handling

        >>> astrometry = AstrometryKstars(tempDir=tempDir,
        >>>                               threadPool=threadpool
        >>>                         )

    """

    __all__ = ['AstrometryKstars',
               ]

    version = '0.4'
    logger = logging.getLogger(__name__)

    def __init__(self, tempDir, threadPool):
        self.tempDir = tempDir
        self.threadPool = threadPool
        self.mutexSolve = PyQt5.QtCore.QMutex()
        self.signals = AstrometrySignals()

        if platform.system() == 'Darwin':
            home = os.environ.get('HOME')
            binPath = '/Applications/kstars.app/Contents/MacOS/astrometry/bin'
            self.binPathSolveField = binPath + '/solve-field'
            self.binPathImage2xy = binPath + '/image2xy'
            self.indexPath = home + '/Library/Application Support/Astrometry'
        elif platform.system() == 'Linux':
            binPath = '/usr/bin'
            self.binPathSolveField = binPath + '/solve-field'
            self.binPathImage2xy = binPath + '/image2xy'
            self.indexPath = '/usr/share/astrometry'
        else:
            self.binPathSolveField = ''
            self.binPathImage2xy = ''
            self.indexPath = ''

        cfgFile = self.tempDir + '/astrometry.cfg'
        with open(cfgFile, 'w+') as outFile:
            outFile.write('cpulimit 300\nadd_path {0}\nautoindex\n'.format(self.indexPath))

    def stringToDegree(self, value):
        if not isinstance(value, str):
            return None
        if not len(value):
            return None
        if value.count('+') > 1:
            return None
        if value.count('-') > 1:
            return None
        # managing different coding
        value = value.replace('*', ' ')
        value = value.replace(':', ' ')
        value = value.replace('deg', ' ')
        value = value.replace('"', ' ')
        value = value.replace('\'', ' ')
        value = value.split()
        try:
            value = [float(x) for x in value]
        except Exception as e:
            self.logger.debug('error: {0}, value: {1}'.format(e, value))
            return None
        sign = 1 if value[0] > 0 else -1
        value[0] = abs(value[0])
        if len(value) == 3:
            value = sign * (value[0] + value[1] / 60 + value[2] / 3600)
            return value
        elif len(value) == 2:
            value = sign * (value[0] + value[1] / 60)
            return value
        else:
            return None

    def convertToHMS(self, value):
        """
        takes the given RA value, which should be in HMS format (but different types) and
        convert it to solve-field readable string in HH:MM:SS

        KEYWORD:   RA
        REFERENCE: NOAO
        HDU:       any
        DATATYPE:  real or string
        UNIT:      deg
        COMMENT:   R.A. of the observation
        DEFINITION: The value field gives the Right Ascension of the
        observation.  It may be expressed either as a floating point number in
        units of decimal degrees, or as a character string in 'HH:MM:SS.sss'
        format where the decimal point and number of fractional digits are
        optional. The coordinate reference frame is given by the RADECSYS
        keyword, and the coordinate epoch is given by the EQUINOX keyword.
        Example: 180.6904 or '12:02:45.7'.

        The value field shall contain a character string giving the
        Right Ascension of the observation in 'hh:mm:ss.sss' format.  The decimal
        point and fractional seconds are optional. The coordinate
        reference frame is given by the RADECSYS keyword, and the coordinate
        epoch is given by the EQUINOX keyword. Example: '13:29:24.00'

        :param value:
        :return: converted value as string
        """

        if not isinstance(value, float):
            value = self.stringToDegree(value)
            if value is None:
                return None
            angle = Angle(hours=value, preference='hours')
        else:
            angle = Angle(degrees=value, preference='hours')

        t = Angle.signed_hms(angle)
        value = '{0:02.0f}:{1:02.0f}:{2:02.0f}'.format(t[1], t[2], t[3])
        return value

    def convertToDMS(self, value):
        """
        takes the given DEC value, which should be in DMS format (but different types) and
        convert it to solve-field readable string in sDD:MM:SS

        KEYWORD:   DEC
        REFERENCE: NOAO
        HDU:       any
        DATATYPE:  real or string
        UNIT:      deg
        COMMENT:   declination of the observed object
        DEFINITION: The value field gives the declination of the
        observation.  It may be expressed either as a floating point number in
        units of decimal degrees, or as a character string in 'dd:mm:ss.sss'
        format where the decimal point and number of fractional digits are
        optional. The coordinate reference frame is given by the RADECSYS
        keyword, and the coordinate epoch is given by the EQUINOX keyword.
        Example: -47.25944 or '-47:15:34.00'.

        :param value:
        :return: converted value as string
        """

        if not isinstance(value, float):
            value = self.stringToDegree(value)

        if value is None:
            return None

        angle = Angle(degrees=value, preference='degrees')

        t = Angle.signed_dms(angle)
        sign = '+' if angle.degrees > 0 else '-'
        value = '{0}{1:02.0f}:{2:02.0f}:{3:02.0f}'.format(sign, t[1], t[2], t[3])
        return value

    def checkAvailability(self):
        """

        :return: True if local solve and components is available
        """

        if not os.path.isfile(self.binPathSolveField):
            self.logger.error(f'{self.binPathSolveField} not found')
            return False
        if not os.path.isfile(self.binPathImage2xy):
            self.logger.error(f'{self.binPathImage2xy} not found')
            return False
        if not glob.glob(self.indexPath + '/index-4*.fits'):
            self.logger.error('no index files found')
            return False
        self.logger.info('solve-field, image2xy and index files available')
        return True

    def _readCheckFitsData(self, fitsPath='', optionalScale=0):
        """
        _readCheckFitsData reads the fits file with the image and tries to get some key
        fields out of the header for preparing the solver. necessary data are

            - 'SCALE': pixel scale in arcsec per pixel
            - 'OBJCTRA' : ra position of the object in HMS format
            - 'OBJCTDEC' : dec position of the object in DMS format

        if OBJCTRA / OBJCTDEC is not readable or not present, we remove the parameters
        to get a blind solve

        :param fitsPath: fits file with image data
        :param optionalScale: optional scaling used, when not scale parameter is in header
        :return: options as string
        """

        if not fitsPath:
            return ''

        with fits.open(fitsPath) as fitsHandle:
            fitsHeader = fitsHandle[0].header
            scale = fitsHeader.get('scale', '0')
            ra = fitsHeader.get('OBJCTRA', '')
            dec = fitsHeader.get('OBJCTDEC', '')

        if scale == 0:
            scale = optionalScale
        ra = self.convertToHMS(ra)
        dec = self.convertToDMS(dec)
        scaleLow = float(scale) * 0.9
        scaleHigh = float(scale) * 1.1

        if not ra or not dec:
            return ''
        options = f' --scale-low {scaleLow} --scale-high {scaleHigh}'
        options += f' --ra {ra} --dec {dec} --radius 1'
        return options

    def _addWCSDataToFits(self, fitsPath=''):
        """
        _addWCSDataToFits reads the fits file containing the wcs data output from solve-field
        and embeds it to the given fits file with image. it removes all entries starting with
        some keywords given in selection. we starting with COMMENT and HISTORY

        :param fitsPath: path to the fits file, where the wcs header should be embedded
        :return: success
        """

        if not fitsPath:
            return False

        remove = ['COMMENT', 'HISTORY']

        wcsFile = self.tempDir + '/temp.wcs'
        with fits.open(fitsPath, mode='update') as fitsHandle:
            fitsHeader = fitsHandle[0].header
            with fits.open(wcsFile) as wcsHandle:
                wcsHeader = wcsHandle[0].header
                fitsHeader.update({k: wcsHeader[k] for k in wcsHeader if k not in remove})
        return True

    @staticmethod
    def _getSolutionFromFits(fitsPath=''):
        """
        _getSolutionFromWCS reads the fits file containing the wcs data and returns the
        basic data needed

        :return: ra in hours, dec in degrees, angle in degrees, scale in arcsec/pixel
        """

        with fits.open(fitsPath) as fitsHandle:
            fitsHeader = fitsHandle[0].header
            wcsObject = WCS(fitsHeader).celestial
            ra = fitsHeader.get('CRVAL1')
            dec = fitsHeader.get('CRVAL2')
            scale = astropy.wcs.utils.proj_plane_pixel_scales(wcsObject)[0] * 3600
            CD1_1 = fitsHeader.get('CD1_1', 0)
            angle = np.degrees(np.arccos(CD1_1))
        ra = ra * 24 / 360
        return ra, dec, angle, scale

    def solve(self, fitsPath=''):
        """
        Solve uses the astrometry.net solver capabilities. The intention is to use an
        offline solving capability, so we need a installed instance. As we go multi
        platform and we need to focus on MW function, we use the astrometry.net package
        which is distributed with KStars / EKOS. Many thanks to them providing such a
        nice package.
        As we go using astrometry.net we focus on the minimum feature set possible to
        omit many of the installation and wrapping work to be done. So we only support
        solving of FITS files, use no python environment for astrometry.net parts (as we
        could access these via MW directly)

        The base outside ideas of implementation come from astrometry.net itself and the
        astrometry implementation from cloudmakers.eu (another nice package for MAC Astro
        software)

        We are using the following command line tools with options:

        image2xy:
            -O (overwriting file)
            -o <output filename>
            <fits file>

        solve-field:
            --overwrite
            --no-plots
            --no-remove-lines
            --no-verify-uniformize
            --sort-column FLUX  (sort for FLUX column)
            --uniformize 0  (disabling it)
            --config <config> (config file name, usually astrometry.cfg)
            xy (the output file from image2xy)


        :param fitsPath:  full path to fits file
        :return: suc, coords, wcsHeader
        """

        xyPath = self.tempDir + '/temp.xy'
        configPath = self.tempDir + '/astrometry.cfg'
        solvedPath = self.tempDir + '/temp.solved'
        wcsPath = self.tempDir + '/temp.wcs'

        solveOptions = self._readCheckFitsData(fitsPath=fitsPath)

        runnable = [self.binPathImage2xy,
                    '-O',
                    '-o',
                    xyPath,
                    fitsPath]

        result = subprocess.run(args=runnable,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )

        self.logger.debug('image2xy return code: '
                          + str(result.returncode)
                          + ' stderr: '
                          + result.stderr.decode()
                          + ' stdout: '
                          + result.stdout.decode().replace('\n', ' ')
                          )

        if result.returncode:
            return 0, 0, 0, 0

        runnable = [self.binPathSolveField,
                    '--overwrite',
                    '--no-plots',
                    '--no-remove-lines',
                    '--no-verify-uniformize',
                    '--overwrite',
                    '--no-plots',
                    '--no-remove-lines',
                    '--no-verify-uniformize',
                    '--uniformize', '0',
                    '--sort-column', 'FLUX',
                    '--scale-units', 'app',
                    '--crpix-center',
                    '--cpulimit', '60',
                    '--config',
                    configPath,
                    xyPath,
                    ]
        for option in solveOptions.split():
            runnable.append(option)

        result = subprocess.run(args=runnable,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )

        self.logger.debug('solve-field return code: '
                          + str(result.returncode)
                          + ' stderr: '
                          + result.stderr.decode()
                          + ' stdout: '
                          + result.stdout.decode().replace('\n', ' ')
                          )
        if result.returncode:
            return 0, 0, 0, 0

        if not (os.path.isfile(solvedPath) and os.path.isfile(wcsPath)):
            self.logger.error('Image [{0}] could not be solved'.format(fitsPath))
            return 0, 0, 0, 0

        self._addWCSDataToFits(fitsPath=fitsPath)

        ra, dec, angle, scale = self._getSolutionFromFits(fitsPath=fitsPath)
        return ra, dec, angle, scale

    def clearSolve(self):
        """
        the cyclic or long lasting tasks for solving the image should not run
        twice for the same data at the same time. so there is a mutex to prevent this
        behaviour.

        :return:
        """

        self.mutexSolve.unlock()
        self.signals.solveDone.emit()

    def solveDone(self):
        self.signals.solveDone.emit()

    def solveResult(self, obj):
        self.signals.solveResult.emit(obj)

    def solveFits(self, fitsPath=''):
        """

        :param fitsPath:
        :return:
        """

        if not os.path.isfile(fitsPath):
            self.signals.solveDone.emit()
            return False
        if not self.checkAvailability():
            self.signals.solveDone.emit()
            return False

        if not self.mutexSolve.tryLock():
            print('overrun')
            self.logger.info('overrun in solve')
            self.signals.solveDone.emit()
            return False

        worker = tpool.Worker(self.solve, fitsPath=fitsPath)
        worker.signals.result.connect(self.solveResult)
        worker.signals.finished.connect(self.clearSolve)
        self.threadPool.start(worker)
        return True


if __name__ == '__main__':
    test = PyQt5.QtWidgets.QApplication([])

    threadPol = PyQt5.QtCore.QThreadPool()
    fitsPath = './mw4/test/config/m51.fit'
    tempDir = './mw4/test/temp/'

    astro = AstrometryKstars(tempDir=tempDir,
                             threadPool=threadPol)

    suc = astro.solveFits(fitsPath=fitsPath)
    print(suc)
    QTest.qWait(5000)