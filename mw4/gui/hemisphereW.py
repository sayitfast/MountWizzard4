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
import bisect
# external packages
import PyQt5
import numpy as np
import matplotlib.path as mpath
import matplotlib.patches as mpatches
# local import
from mw4.gui import widget
from mw4.gui.widgets import hemisphere_ui


class HemisphereWindow(widget.MWidget):
    """
    the hemisphere window class handles

    """

    __all__ = ['HemisphereWindow',
               ]
    version = '0.1'
    logger = logging.getLogger(__name__)

    CYCLE_GUI = 3000
    BACK = 'background-color: transparent;'
    MODE = dict(
        normal=dict(horMarker='None',
                    horColor='#006000',
                    buildPColor='#00A000',
                    starSize=6,
                    starColor='#808000',
                    starAnnColor='#808080'),
        build=dict(horMarker='None',
                   horColor='#006000',
                   buildPColor='#FF00FF',
                   starSize=6,
                   starColor='#808000',
                   starAnnColor='#808080'),
        horizon=dict(horMarker='o',
                     horColor='#FF00FF',
                     buildPColor='#004000',
                     starSize=6,
                     starColor='#808000',
                     starAnnColor='#808080'),
        star=dict(horMarker='None',
                  horColor='#003000',
                  buildPColor='#004000',
                  starSize=12,
                  starColor='#FFFF00',
                  starAnnColor='#F0F0F0')
    )

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.showStatus = False
        self.ui = hemisphere_ui.Ui_HemisphereDialog()
        self.ui.setupUi(self)
        self.initUI()

        # attributes to be stored in class
        self.pointerAltAz = None
        self.pointerDome = None
        self.pointsBuild = None
        self.pointsBuildAnnotate = list()
        self.starsAlign = None
        self.starsAlignAnnotate = list()
        self.horizonFill = None
        self.horizonMarker = None
        self.meridianSlew = None
        self.meridianTrack = None
        self.celestialPath = None

        # doing the matplotlib embedding
        # for the alt az plane
        self.hemisphereMat = self.embedMatplot(self.ui.hemisphere)
        self.hemisphereMat.parentWidget().setStyleSheet(self.BACK)
        self.clearRect(self.hemisphereMat, True)
        # for the fast moving parts
        self.hemisphereMatM = self.embedMatplot(self.ui.hemisphereM)
        self.hemisphereMatM.parentWidget().setStyleSheet(self.BACK)
        self.clearRect(self.hemisphereMatM, False)
        # for the stars in background
        self.hemisphereMatS = self.embedMatplot(self.ui.hemisphereS)
        self.hemisphereMatS.parentWidget().setStyleSheet(self.BACK)
        self.ui.hemisphereS.setVisible(True)
        self.clearRect(self.hemisphereMatS, False)

        # signals for gui
        self.ui.checkShowSlewPath.clicked.connect(self.drawHemisphere)
        self.ui.checkShowMeridian.clicked.connect(self.updateMeridian)
        self.ui.checkShowCelestial.clicked.connect(self.updateCelestialPath)
        self.app.redrawHemisphere.connect(self.drawHemisphere)
        self.app.mount.signals.pointDone.connect(self.updatePointerAltAz)
        self.app.mount.signals.pointDone.connect(self.updateDome)
        self.app.mount.signals.settDone.connect(self.updateMeridian)
        self.app.mount.signals.settDone.connect(self.updateCelestialPath)
        self.ui.clearBuildP.clicked.connect(self.clearHemisphere)
        self.app.mainW.ui.checkUseHorizon.clicked.connect(self.drawHemisphere)
        self.ui.checkEditNone.clicked.connect(self.setOperationMode)
        self.ui.checkEditHorizonMask.clicked.connect(self.setOperationMode)
        self.ui.checkEditBuildPoints.clicked.connect(self.setOperationMode)
        self.ui.checkPolarAlignment.clicked.connect(self.setOperationMode)
        self.ui.checkShowAlignStar.clicked.connect(self.drawHemisphere)
        self.ui.checkShowAlignStar.clicked.connect(self.configOperationMode)

        if 'mainW' in self.app.config:
            fileName = self.app.config['mainW'].get('horizonFileName')
            self.app.data.loadHorizonP(fileName=fileName)
        self.initConfig()
        self.configOperationMode()

        # setting up the timers
        self.timerGui = PyQt5.QtCore.QTimer()
        self.timerGui.setSingleShot(False)
        self.timerGui.timeout.connect(self.updateGUI)
        self.timerGui.start(self.CYCLE_GUI)

    def initConfig(self):
        if 'hemisphereW' not in self.app.config:
            return False
        config = self.app.config['hemisphereW']
        x = config.get('winPosX', 100)
        y = config.get('winPosY', 100)
        if x > self.screenSizeX:
            x = 0
        if y > self.screenSizeY:
            y = 0
        self.move(x, y)
        height = config.get('height', 600)
        width = config.get('width', 800)
        self.resize(width, height)
        self.ui.checkShowSlewPath.setChecked(config.get('checkShowSlewPath', False))
        self.ui.checkShowMeridian.setChecked(config.get('checkShowMeridian', False))
        self.ui.checkShowCelestial.setChecked(config.get('checkShowCelestial', False))
        self.ui.checkShowAlignStar.setChecked(config.get('checkShowAlignStar', False))
        if config.get('showStatus'):
            self.showWindow()
        return True

    def storeConfig(self):
        if 'hemisphereW' not in self.app.config:
            self.app.config['hemisphereW'] = {}
        config = self.app.config['hemisphereW']
        config['winPosX'] = self.pos().x()
        config['winPosY'] = self.pos().y()
        config['height'] = self.height()
        config['width'] = self.width()
        config['showStatus'] = self.showStatus
        config['checkShowSlewPath'] = self.ui.checkShowSlewPath.isChecked()
        config['checkShowMeridian'] = self.ui.checkShowMeridian.isChecked()
        config['checkShowCelestial'] = self.ui.checkShowCelestial.isChecked()
        config['checkShowAlignStar'] = self.ui.checkShowAlignStar.isChecked()

    def resizeEvent(self, QResizeEvent):
        """
        resizeEvent changes the internal widget according to the resize of the window
        the formulae of the calculation is:
            spaces left right top button : 5 pixel
            widget start in height at y = 130

        :param QResizeEvent:
        :return: nothing
        """

        super().resizeEvent(QResizeEvent)
        space = 5
        startY = 130
        self.ui.hemisphere.setGeometry(space,
                                       startY - space,
                                       self.width() - 2 * space,
                                       self.height() - startY)
        self.ui.hemisphereS.setGeometry(space,
                                        startY - space,
                                        self.width() - 2 * space,
                                        self.height() - startY)
        self.ui.hemisphereM.setGeometry(space,
                                        startY - space,
                                        self.width() - 2 * space,
                                        self.height() - startY)

    def closeEvent(self, closeEvent):
        super().closeEvent(closeEvent)
        self.changeStyleDynamic(self.app.mainW.ui.openHemisphereW, 'running', 'false')

    def toggleWindow(self):
        self.showStatus = not self.showStatus
        if self.showStatus:
            self.showWindow()
        else:
            self.close()

    def showWindow(self):
        self.showStatus = True
        self.drawHemisphere()
        self.show()
        self.changeStyleDynamic(self.app.mainW.ui.openHemisphereW, 'running', 'true')

    def updateGUI(self):
        """
        updateGUI update gui elements on regular bases (actually 10 second) for items,
        which are not events based.

        :return: success
        """

        self.updateAlignStar()
        return True

    @staticmethod
    def clearAxes(axes, visible=False):
        axes.cla()
        axes.set_facecolor((0, 0, 0, 0))
        axes.set_xlim(0, 360)
        axes.set_ylim(0, 90)
        if not visible:
            axes.set_axis_off()
            return False
        axes.spines['bottom'].set_color('#2090C0')
        axes.spines['top'].set_color('#2090C0')
        axes.spines['left'].set_color('#2090C0')
        axes.spines['right'].set_color('#2090C0')
        axes.grid(True, color='#404040')
        axes.set_facecolor((0, 0, 0, 0))
        axes.tick_params(axis='x',
                         colors='#2090C0',
                         labelsize=12)
        axes.set_xlim(0, 360)
        axes.set_xticks(np.arange(0, 361, 30))
        axes.set_ylim(0, 90)
        axes.tick_params(axis='y',
                         colors='#2090C0',
                         which='both',
                         labelleft=True,
                         labelright=True,
                         labelsize=12)
        axes.set_xlabel('Azimuth in degrees',
                        color='#2090C0',
                        fontweight='bold',
                        fontsize=12)
        axes.set_ylabel('Altitude in degrees',
                        color='#2090C0',
                        fontweight='bold',
                        fontsize=12)
        return True

    def drawCanvas(self):
        """
        drawCanvas retrieves the static content axes from widget and redraws the canvas

        :return: success for test
        """

        axes = self.hemisphereMat.figure.axes[0]
        axes.figure.canvas.draw()
        return True

    def drawCanvasMoving(self):
        """
        drawCanvasMoving retrieves the moving content axes from widget and redraws the
        canvas

        :return: success for test
        """

        axesM = self.hemisphereMatM.figure.axes[0]
        axesM.figure.canvas.draw()
        return True

    def drawCanvasStar(self):
        """
        drawCanvasStar retrieves the moving content axes from widget and redraws the canvas

        :return: success for test
        """

        axesS = self.hemisphereMatS.figure.axes[0]
        axesS.figure.canvas.draw()
        return True

    def updateCelestialPath(self):
        """
        updateCelestialPath is called whenever an update of settings from mount are given.
        it takes the actual values and corrects the point in window if window is in
        show status.

        :return: success for testing
        """

        if not self.showStatus:
            return False
        if self.celestialPath is None:
            return False
        self.celestialPath.set_visible(self.ui.checkShowCelestial.isChecked())
        self.drawCanvas()
        return True

    def updateMeridian(self):
        """
        updateMeridian is called whenever an update of settings from mount are given. it
        takes the actual values and corrects the point in window if window is in
        show status.

        :return: success
        """

        if not self.showStatus:
            return False
        slew = self.app.mount.sett.meridianLimitSlew
        track = self.app.mount.sett.meridianLimitTrack
        if slew is None or track is None:
            return False
        self.meridianTrack.set_visible(self.ui.checkShowMeridian.isChecked())
        self.meridianSlew.set_visible(self.ui.checkShowMeridian.isChecked())
        self.meridianTrack.set_xy((180 - track, 0))
        self.meridianSlew.set_xy((180 - slew, 0))
        self.meridianTrack.set_width(2 * track)
        self.meridianSlew.set_width(2 * slew)
        self.drawCanvas()
        return True

    def updatePointerAltAz(self):
        """
        updatePointerAltAz is called whenever an update of coordinates from mount are
        given. it takes the actual values and corrects the point in window if window is in
        show status.

        :return: success
        """

        if not self.showStatus:
            return False
        obsSite = self.app.mount.obsSite
        if obsSite.Alt is None:
            return False
        if obsSite.Az is None:
            return False
        alt = obsSite.Alt.degrees
        az = obsSite.Az.degrees
        self.pointerAltAz.set_data((az, alt))
        self.pointerAltAz.set_visible(True)
        self.drawCanvasMoving()
        return True

    def updateDome(self):
        """
        updateDome is called whenever an update of coordinates from dome are given.
        it takes the actual values and corrects the point in window if window is in
        show status.

        :return: success
        """

        if not self.showStatus:
            return False

        # using mount for test
        obsSite = self.app.mount.obsSite
        if obsSite.Az is None:
            return False
        az = obsSite.Az.degrees

        self.pointerDome.set_xy((az - 15, 0))
        self.pointerDome.set_visible(True)
        self.drawCanvasMoving()
        return True

    def updateAlignStar(self):
        """
        updateAlignStar is called whenever an update of coordinates from mount are
        given. it takes the actual values and corrects the point in window if window is in
        show status.

        :return: success
        """

        if not self.showStatus:
            return False
        if self.starsAlign is None:
            return False
        if not self.ui.checkShowAlignStar.isChecked():
            return False
        hip = self.app.hipparcos
        hip.calculateAlignStarPositionsAltAz()
        self.starsAlign.set_data(hip.az, hip.alt)
        for i, starAnnotation in enumerate(self.starsAlignAnnotate):
            starAnnotation.set_anncoords('data')
            starAnnotation.set_position((hip.az[i], hip.alt[i]))
        self.drawCanvasStar()
        return True

    @staticmethod
    def markerPoint():
        """
        markerPoint constructs a custom marker for presentation of modeldata points

        :return: marker
        """

        circleB = mpath.Path.unit_circle()
        circleS = mpath.Path.unit_circle()
        # concatenate the circle with an internal cutout of the star
        verts = np.concatenate([circleB.vertices, 0.5 * circleS.vertices])
        codes = np.concatenate([circleB.codes, circleS.codes])
        marker = mpath.Path(verts, codes)
        return marker

    @staticmethod
    def markerAltAz():
        """
        markerAltAz constructs a custom marker for AltAz pointer

        :return: marker
        """

        circleB = mpath.Path.unit_circle()
        circleM = mpath.Path.unit_circle()
        circleS = mpath.Path.unit_circle()
        # concatenate the circle with an internal cutout of the star
        verts = np.concatenate([circleB.vertices,
                                0.8 * circleM.vertices,
                                0.3 * circleS.vertices])
        codes = np.concatenate([circleB.codes,
                                circleM.codes,
                                circleS.codes])
        marker = mpath.Path(verts, codes)
        return marker

    @staticmethod
    def markerStar():
        """
        markerStar constructs a custom marker for presentation of modeldata points

        :return: marker
        """

        star = mpath.Path.unit_regular_star(8)
        # concatenate the circle with an internal cutout of the star
        verts = np.concatenate([star.vertices])
        codes = np.concatenate([star.codes])
        marker = mpath.Path(verts, codes)
        return marker

    def clearHemisphere(self):
        """
        clearHemisphere is called when after startup the location of the mount is changed
        to reconstruct correctly the hemisphere window

        :return:
        """

        self.pointsBuild = None
        self.pointsBuildAnnotate = list()
        self.app.data.clearBuildP()
        self.drawHemisphere()

    def configOperationMode(self):
        """
        configOperationMode enables and disables the select PolarAlign button according
        to the status of Show align stars. without showing align stars it does not make
        sense to enable this function.

        :return: nothing
        """

        if self.ui.checkShowAlignStar.isChecked():
            self.ui.checkPolarAlignment.setEnabled(True)
        else:
            self.ui.checkPolarAlignment.setEnabled(False)
            if self.ui.checkPolarAlignment.isChecked():
                self.ui.checkEditNone.setChecked(True)

    def setOperationMode(self):
        """
        setOperationMode changes the operation mode of the hemisphere window(s) depending
        on the choice, colors and styles will be changed. this also is valid for the stacking
        order of the widgets

        normal mode:    hemisphereM is on top,
                        hemisphere is next,
                        hemisphereS is bottom
        edit mode:      hemisphere is on top,
                        hemisphereM is next,
                        hemisphereS is bottom
        horizon mode:   hemisphere is on top,
                        hemisphereM is next,
                        hemisphereS is bottom
        star mode:      hemisphereS is on top,
                        hemisphereM is next,
                        hemisphere is bottom

        :return: success
        """

        mode = ''
        if self.ui.checkEditNone.isChecked():
            mode = 'normal'
        elif self.ui.checkEditBuildPoints.isChecked():
            mode = 'build'
        elif self.ui.checkEditHorizonMask.isChecked():
            mode = 'horizon'
        elif self.ui.checkPolarAlignment.isChecked():
            mode = 'star'

        # styles
        if self.horizonMarker is not None:
            self.horizonMarker.set_marker(self.MODE[mode]['horMarker'])
            self.horizonMarker.set_color(self.MODE[mode]['horColor'])
        if self.pointsBuild is not None:
            self.pointsBuild.set_color(self.MODE[mode]['buildPColor'])
        if self.starsAlign is not None:
            # self.starsAlignAnnotate.set_color(self.MODE[mode]['horMarker'])
            self.starsAlign.set_color(self.MODE[mode]['starColor'])

        # stacking of widgets in the right order for managing the mouse events right
        if mode is 'star':
            self.ui.hemisphere.raise_()
            self.ui.hemisphereM.raise_()
            self.ui.hemisphereS.raise_()
        elif mode is 'normal':
            self.ui.hemisphereS.raise_()
            self.ui.hemisphere.raise_()
            self.ui.hemisphereM.raise_()
        else:
            self.ui.hemisphereS.raise_()
            self.ui.hemisphereM.raise_()
            self.ui.hemisphere.raise_()

        self.drawCanvas()
        self.drawCanvasStar()
        return True

    @staticmethod
    def getIndexPoint(event=None, plane=None, epsilon=2):
        """
        getIndexPoint returns the index of the point which is nearest to the coordinate
        of the mouse click when the click is in distance epsilon of the points. otherwise
        no index will be returned.

        :param event: data of the mouse clicked event
        :param plane: coordinates as tuples (alt, az)
        :param epsilon:
        :return: index or none
        """

        if event is None:
            return None
        if plane is None:
            return None
        if len(plane) == 0:
            return None

        xt = np.asarray([i[1] for i in plane])
        yt = np.asarray([i[0] for i in plane])
        d = np.sqrt((xt - event.xdata)**2 / 16 + (yt - event.ydata)**2)
        index = d.argsort()[:1][0]
        # position to far away
        if d[index] >= epsilon:
            return None
        index = int(index)
        return index

    @staticmethod
    def getIndexPointX(event=None, plane=None):
        """
        getIndexPointX returns the index of the point which has a x coordinate closest to
        the left of the x coordinate of the mouse click regardless which y coordinate it has

        :param event: data of the mouse clicked event
        :param plane: coordinates as tuples (x, y)
        :return: index or none
        """

        if event is None:
            return None
        if plane is None:
            return None
        if len(plane) < 2:
            return None

        xt = [i[1] for i in plane]
        index = int(bisect.bisect_left(xt, event.xdata) - 1)
        return index

    def onMouseNormal(self, event):
        """
        onMouseNormal handles the mouse event in normal mode. this means only a double
        click is possible and offers the opportunity to slew the telescope to a certain
        position in sky selected by the mouse.

        :param event: mouse events
        :return: success
        """

        if not event.inaxes:
            return False
        if event.button != 1 or not event.dblclick:
            return False

        textFormat = 'Do you want to slew the mount to:\n\nAzimuth:\t{0}°\nAltitude:\t{1}°'
        azimuth = int(event.xdata + 0.5)
        altitude = int(event.ydata + 0.5)
        question = textFormat.format(azimuth, altitude)
        msg = PyQt5.QtWidgets.QMessageBox
        reply = msg.question(self,
                             'Hemisphere direct slew',
                             question,
                             msg.Yes | msg.No,
                             msg.No,
                             )
        if reply != msg.Yes:
            return False
        suc = self.app.mount.obsSite.slewAltAz(alt_degrees=altitude,
                                               az_degrees=azimuth,
                                               slewType='normal')
        if not suc:
            self.app.message.emit('Cannot slew to: {0}, {1}'.format(azimuth, altitude), 2)
        else:
            self.app.message.emit('Slewing to: {0}, {1}'.format(azimuth, altitude), 0)
        return suc

    def addHorizonPoint(self, data=None, event=None):
        """
        addHorizonPoint calculates from the position of the left mouse click the position
        where the next horizon point should be added. the coordinates are given from mouse
        click itself.

        :param data: point in tuples (alt, az)
        :param event: mouse event
        :return:
        """

        index = self.getIndexPointX(event=event, plane=data.horizonP) + 1
        suc = data.addHorizonP(value=(event.ydata, event.xdata),
                               position=index)
        return suc

    def deleteHorizonPoint(self, data=None, event=None):
        """
        deleteHorizonPoint selects the next horizon point in distance max and tries to
        delete it. there have to be at least 2 horizon point left.

        :param data: point in tuples (alt, az)
        :param event: mouse event
        :return: success
        """

        index = self.getIndexPoint(event=event, plane=data.horizonP)
        suc = False
        if len(data.horizonP) > 2:
            suc = data.delHorizonP(position=index)
        return suc

    def editHorizonMask(self, data=None, event=None):
        """
        editHorizonMask does dispatching the different mouse clicks for adding or deleting
        horizon mask points and call the function accordingly.

        :param data: point in tuples (alt, az)
        :param event: mouse event
        :return: success
        """

        if event.button == 1:
            suc = self.addHorizonPoint(data=data, event=event)
        elif event.button == 3:
            suc = self.deleteHorizonPoint(data=data, event=event)
        else:
            return False

        y, x = zip(*data.horizonP)
        self.horizonMarker.set_data(x, y)
        self.horizonFill.set_xy(np.column_stack((x, y)))

        self.drawCanvas()
        return suc

    def addBuildPoint(self, data=None, event=None, axes=None):
        """
        addBuildPoint calculates from the position of the left mouse click the position
        where the next modeldata point should be added. the coordinates are given from mouse
        click itself.

        :param data: point in tuples (alt, az)
        :param event: mouse event
        :param axes: link to drawing axes in matplotlib
        :return:
        """

        index = self.getIndexPoint(event=event, plane=data.buildP, epsilon=360)
        # if no point found, add at the end
        if index is None:
            index = len(data.buildP)
        # take the found point closer to the end of the list
        index += 1
        suc = data.addBuildP(value=(event.ydata, event.xdata),
                             position=index)
        if not suc:
            return False

        # if succeeded, than add the data to the matplotlib hemisphere widget
        # first the point
        x = event.xdata
        y = event.ydata
        if self.ui.checkShowSlewPath.isChecked():
            ls = ':'
            lw = 1
        else:
            ls = ''
            lw = 0
        color = '#FF00FF'
        if self.pointsBuild is None:
            newBuildP, = axes.plot(x,
                                   y,
                                   marker=self.markerPoint(),
                                   markersize=9,
                                   linestyle=ls,
                                   lw=lw,
                                   fillstyle='none',
                                   color=color,
                                   zorder=20,
                                   )
            self.pointsBuild = newBuildP

        # and than the annotation (number)
        xy = (x, y)
        newAnnotation = axes.annotate('4',
                                      xy=xy,
                                      xytext=(2, -10),
                                      textcoords='offset points',
                                      color='#E0E0E0',
                                      zorder=10,
                                      )
        if self.pointsBuildAnnotate is None:
            self.pointsBuildAnnotate = list()
        self.pointsBuildAnnotate.insert(index, newAnnotation)
        return True

    def deleteBuildPoint(self, data=None, event=None):
        """
        deleteBuildPoint selects the next modeldata point in distance max and tries to
        delete it. there have to be at least 2 horizon point left.

        :param data: point in tuples (alt, az)
        :param event: mouse event
        :return: success
        """

        index = self.getIndexPoint(event=event, plane=data.buildP)
        suc = data.delBuildP(position=index)
        if suc:
            self.pointsBuildAnnotate[index].remove()
            del self.pointsBuildAnnotate[index]
        return suc

    def editBuildPoints(self, data=None, event=None, axes=None):
        """
        editBuildPoints does dispatching the different mouse clicks for adding or deleting
        modeldata points and call the function accordingly.

        :param data: points in tuples (alt, az)
        :param event: mouse event
        :param axes: link to drawing axes in matplotlib
        :return: success
        """

        if event.button == 1:
            suc = self.addBuildPoint(data=data, event=event, axes=axes)
        elif event.button == 3:
            suc = self.deleteBuildPoint(data=data, event=event)
        else:
            return False

        # redraw the corrected canvas (new positions ans new numbers)
        if len(data.buildP):
            y, x = zip(*data.buildP)
        else:
            y = x = []
        self.pointsBuild.set_data(x, y)
        for i, _ in enumerate(data.buildP):
            self.pointsBuildAnnotate[i].set_text('{0:2d}'.format(i + 1))
        self.drawCanvas()
        return suc

    def onMouseEdit(self, event):
        """
        onMouseEdit handles the mouse event in normal mode. this means depending on the
        edit mode (horizon or model points) a left click adds a new point and right click
        deletes the selected point.

        :param event: mouse events
        :return: success
        """

        data = self.app.data
        axes = self.hemisphereMat.figure.axes[0].axes

        if not event.inaxes:
            return False
        if event.dblclick:
            return False

        if self.ui.checkEditHorizonMask.isChecked():
            suc = self.editHorizonMask(event=event, data=data)
        elif self.ui.checkEditBuildPoints.isChecked():
            suc = self.editBuildPoints(event=event, data=data, axes=axes)
        else:
            return False
        return suc

    def onMouseStar(self, event):
        """
        onMouseStar handles the mouse event in polar align mode. this means only a right
        click is possible and offers the opportunity to slew the telescope to the selected
        star and start manual polar alignment.

        :param event: mouse events
        :return: success
        """

        if not event.inaxes:
            return False
        if event.button != 1:
            return False
        if event.dblclick:
            return False

        hip = self.app.hipparcos
        plane = list(zip(hip.alt, hip.az))
        index = self.getIndexPoint(event=event, plane=plane, epsilon=2)
        if index is None:
            return False

        name = hip.name[index]
        textFormat = 'Do you want to slew the mount to:\n\n{0}'
        question = textFormat.format(name)
        msg = PyQt5.QtWidgets.QMessageBox
        reply = msg.question(self,
                             'Hemisphere polar align',
                             question,
                             msg.Yes | msg.No,
                             msg.No,
                             )
        if reply != msg.Yes:
            return False
        ra, dec = hip.getAlignStarRaDecFromName(hip.name[index])
        suc = self.app.mount.obsSite.slewRaDec(ra_hours=ra,
                                               dec_degrees=dec,
                                               slewType='polar')
        if not suc:
            self.app.message.emit('Cannot slew to: {0}'.format(name), 2)
        else:
            self.app.message.emit('Slewing to: {0}'.format(name), 0)
        return suc

    def drawHemisphereStatic(self, axes=None):
        """
         drawHemisphereStatic renders the static part of the hemisphere window and puts
         all drawing on the static plane. the content consist of:
            - modeldata points
            - horizon mask
            - celestial paths
            - meridian limits
        with all their styles an coloring

        :param axes: matplotlib axes object
        :return:
        """

        # drawing horizon
        showHorizon = self.app.mainW.ui.checkUseHorizon.isChecked()
        if self.app.data.horizonP and showHorizon:
            alt, az = zip(*self.app.data.horizonP)

            self.horizonFill, = axes.fill(az, alt, color='#002000', zorder=-20)
            self.horizonMarker, = axes.plot(az, alt, color='#006000', zorder=-20, lw=3)
            if self.ui.checkEditHorizonMask.isChecked():
                self.horizonMarker.set_marker('o')
                self.horizonMarker.set_color('#FF00FF')

        # drawing modeldata points
        if self.app.data.buildP:
            alt, az = zip(*self.app.data.buildP)
            # show line path pf slewing
            if self.ui.checkShowSlewPath.isChecked():
                ls = ':'
                lw = 1
            else:
                ls = ''
                lw = 0
            if self.ui.checkEditBuildPoints.isChecked():
                color = '#FF00FF'
            else:
                color = '#00A000'
            self.pointsBuild, = axes.plot(az, alt,
                                          marker=self.markerPoint(),
                                          markersize=9,
                                          linestyle=ls,
                                          lw=lw,
                                          fillstyle='none',
                                          color=color,
                                          zorder=20,
                                          )
            self.pointsBuildAnnotate = list()
            for i, AltAz in enumerate(zip(az, alt)):
                annotation = axes.annotate('{0:2d}'.format(i + 1),
                                           xy=AltAz,
                                           xytext=(2, -10),
                                           textcoords='offset points',
                                           color='#E0E0E0',
                                           zorder=10,
                                           )
                self.pointsBuildAnnotate.append(annotation)

        # draw celestial equator
        visible = self.ui.checkShowCelestial.isChecked()
        celestial = self.app.data.generateCelestialEquator()
        alt, az = zip(*celestial)
        self.celestialPath, = axes.plot(az,
                                        alt,
                                        '.',
                                        markersize=1,
                                        fillstyle='none',
                                        color='#808080',
                                        visible=visible)
        # draw meridian limits
        if self.app.mount.sett.meridianLimitSlew is not None:
            slew = self.app.mount.sett.meridianLimitSlew
        else:
            slew = 0
        visible = self.ui.checkShowMeridian.isChecked()
        self.meridianSlew = mpatches.Rectangle((180 - slew, 0),
                                               2 * slew,
                                               90,
                                               zorder=-5,
                                               color='#FF000040',
                                               lw=1,
                                               fill=True,
                                               visible=visible)
        axes.add_patch(self.meridianSlew)
        if self.app.mount.sett.meridianLimitTrack is not None:
            track = self.app.mount.sett.meridianLimitTrack
        else:
            track = 0
        self.meridianTrack = mpatches.Rectangle((180 - track, 0),
                                                2 * track,
                                                90,
                                                zorder=-10,
                                                color='#FFFF0040',
                                                lw=1,
                                                fill=True,
                                                visible=visible)
        axes.add_patch(self.meridianTrack)

    def drawHemisphereMoving(self, axes=None):
        """
        drawHemisphereMoving is rendering the moving part which consists of:
            - pointer: where the mount points to
            - dome widget: which shows the position of the dome opening
        the dynamic ones are located on a separate plane to improve rendering speed,
        because we update this part very often.

        :param axes: matplotlib axes object
        :return:
        """

        # pointer
        self.pointerAltAz, = axes.plot(180, 45,
                                       zorder=10,
                                       color='#FF00FF',
                                       marker=self.markerAltAz(),
                                       markersize=25,
                                       linestyle='none',
                                       fillstyle='none',
                                       clip_on=False,
                                       visible=False,
                                       )
        # adding pointer of dome if dome is present
        self.pointerDome = mpatches.Rectangle((165, 0),
                                              30,
                                              90,
                                              zorder=-30,
                                              color='#40404080',
                                              lw=3,
                                              fill=True,
                                              visible=False)
        axes.add_patch(self.pointerDome)

    def drawHemisphereStars(self, axes=None):
        """
        drawHemisphereStars is rendering the alignment star map. this moves over time with
        the speed of earth turning. so we have to update the rendering, but on low speed
        without having any user interaction.

        :param axes: matplotlib axes object
        :return:
        """

        visible = self.ui.checkShowAlignStar.isChecked()
        self.starsAlignAnnotate = list()
        hip = self.app.hipparcos
        hip.calculateAlignStarPositionsAltAz()
        self.starsAlign, = axes.plot(hip.az,
                                     hip.alt,
                                     marker=self.markerStar(),
                                     markersize=7,
                                     linestyle='',
                                     color='#808000',
                                     zorder=-20,
                                     visible=visible,
                                     )
        for alt, az, name in zip(hip.alt, hip.az, hip.name):
            annotation = axes.annotate(name,
                                       xy=(az, alt),
                                       xytext=(0, 0),
                                       textcoords='offset points',
                                       xycoords='data',
                                       color='#808080',
                                       fontsize=12,
                                       clip_on=True,
                                       visible=visible,
                                       )
            self.starsAlignAnnotate.append(annotation)

    def drawHemisphere(self):
        """
        drawHemisphere is the basic renderer for all items and widgets in the hemisphere
        window. it takes care of drawing the grid, enables three layers of transparent
        widgets for static content, moving content and star maps. this is mainly done to
        get a reasonable performance when redrawing the canvas. in addition it initializes
        the objects for points markers, patches, lines etc. for making the window nice
        and user friendly.
        the user interaction on the hemisphere windows is done by the event handler of
        matplotlib itself implementing an on Mouse handler, which takes care of functions.

        :return: nothing
        """

        # shortening the references
        axes = self.hemisphereMat.figure.axes[0]
        axesM = self.hemisphereMatM.figure.axes[0]
        axesS = self.hemisphereMatS.figure.axes[0]

        # clearing axes before drawing, only static visible, dynamic only when content
        # is available. visibility is handled with their update method
        self.clearAxes(axes, visible=True)
        self.clearAxes(axesM, visible=False)
        self.clearAxes(axesS, visible=False)

        # calling renderer
        self.drawHemisphereStatic(axes=axes)
        self.drawHemisphereMoving(axes=axesM)
        self.drawHemisphereStars(axes=axesS)

        self.setOperationMode()

        # drawing the canvas
        axes.figure.canvas.draw()
        axesM.figure.canvas.draw()
        axesS.figure.canvas.draw()

        # finally setting the mouse handler
        self.hemisphereMat.figure.canvas.mpl_connect('button_press_event',
                                                     self.onMouseEdit)
        self.hemisphereMatM.figure.canvas.mpl_connect('button_press_event',
                                                      self.onMouseNormal)
        self.hemisphereMatS.figure.canvas.mpl_connect('button_press_event',
                                                      self.onMouseStar)