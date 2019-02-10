# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'image.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImageDialog(object):
    def setupUi(self, ImageDialog):
        ImageDialog.setObjectName("ImageDialog")
        ImageDialog.resize(800, 600)
        ImageDialog.setMinimumSize(QtCore.QSize(800, 600))
        ImageDialog.setMaximumSize(QtCore.QSize(1600, 1200))
        font = QtGui.QFont()
        font.setFamily("Arial")
        ImageDialog.setFont(font)
        self.image = QtWidgets.QWidget(ImageDialog)
        self.image.setGeometry(QtCore.QRect(5, 124, 790, 471))
        self.image.setMinimumSize(QtCore.QSize(690, 270))
        self.image.setMaximumSize(QtCore.QSize(1510, 1070))
        self.image.setAutoFillBackground(True)
        self.image.setObjectName("image")
        self.expose = QtWidgets.QPushButton(ImageDialog)
        self.expose.setGeometry(QtCore.QRect(10, 15, 76, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.expose.sizePolicy().hasHeightForWidth())
        self.expose.setSizePolicy(sizePolicy)
        self.expose.setMinimumSize(QtCore.QSize(76, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.expose.setFont(font)
        self.expose.setObjectName("expose")
        self.solve = QtWidgets.QPushButton(ImageDialog)
        self.solve.setGeometry(QtCore.QRect(90, 15, 76, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.solve.setFont(font)
        self.solve.setObjectName("solve")
        self.load = QtWidgets.QPushButton(ImageDialog)
        self.load.setEnabled(True)
        self.load.setGeometry(QtCore.QRect(10, 45, 76, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.load.setFont(font)
        self.load.setObjectName("load")
        self.stop = QtWidgets.QPushButton(ImageDialog)
        self.stop.setEnabled(False)
        self.stop.setGeometry(QtCore.QRect(250, 15, 76, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.stop.setFont(font)
        self.stop.setObjectName("stop")
        self.imageFileName = QtWidgets.QLineEdit(ImageDialog)
        self.imageFileName.setEnabled(False)
        self.imageFileName.setGeometry(QtCore.QRect(90, 45, 236, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.imageFileName.setFont(font)
        self.imageFileName.setMouseTracking(False)
        self.imageFileName.setFocusPolicy(QtCore.Qt.NoFocus)
        self.imageFileName.setAcceptDrops(False)
        self.imageFileName.setText("")
        self.imageFileName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.imageFileName.setReadOnly(True)
        self.imageFileName.setObjectName("imageFileName")
        self.exposeN = QtWidgets.QPushButton(ImageDialog)
        self.exposeN.setGeometry(QtCore.QRect(170, 15, 76, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.exposeN.setFont(font)
        self.exposeN.setObjectName("exposeN")
        self.line_71 = QtWidgets.QFrame(ImageDialog)
        self.line_71.setGeometry(QtCore.QRect(5, 120, 791, 1))
        self.line_71.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_71.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_71.setObjectName("line_71")
        self.groupBox = QtWidgets.QGroupBox(ImageDialog)
        self.groupBox.setGeometry(QtCore.QRect(360, 10, 431, 106))
        self.groupBox.setObjectName("groupBox")
        self.ccdTemp = QtWidgets.QLineEdit(self.groupBox)
        self.ccdTemp.setEnabled(False)
        self.ccdTemp.setGeometry(QtCore.QRect(345, 60, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.ccdTemp.setFont(font)
        self.ccdTemp.setMouseTracking(False)
        self.ccdTemp.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ccdTemp.setAcceptDrops(False)
        self.ccdTemp.setText("")
        self.ccdTemp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ccdTemp.setReadOnly(True)
        self.ccdTemp.setObjectName("ccdTemp")
        self.expTime = QtWidgets.QLineEdit(self.groupBox)
        self.expTime.setEnabled(False)
        self.expTime.setGeometry(QtCore.QRect(90, 30, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.expTime.setFont(font)
        self.expTime.setMouseTracking(False)
        self.expTime.setFocusPolicy(QtCore.Qt.NoFocus)
        self.expTime.setAcceptDrops(False)
        self.expTime.setText("")
        self.expTime.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.expTime.setReadOnly(True)
        self.expTime.setObjectName("expTime")
        self.binY = QtWidgets.QLineEdit(self.groupBox)
        self.binY.setEnabled(False)
        self.binY.setGeometry(QtCore.QRect(305, 60, 36, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.binY.setFont(font)
        self.binY.setMouseTracking(False)
        self.binY.setFocusPolicy(QtCore.Qt.NoFocus)
        self.binY.setAcceptDrops(False)
        self.binY.setText("")
        self.binY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.binY.setReadOnly(True)
        self.binY.setObjectName("binY")
        self.ra = QtWidgets.QLineEdit(self.groupBox)
        self.ra.setEnabled(False)
        self.ra.setGeometry(QtCore.QRect(5, 60, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.ra.setFont(font)
        self.ra.setMouseTracking(False)
        self.ra.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ra.setAcceptDrops(False)
        self.ra.setText("")
        self.ra.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ra.setReadOnly(True)
        self.ra.setObjectName("ra")
        self.label_38 = QtWidgets.QLabel(self.groupBox)
        self.label_38.setGeometry(QtCore.QRect(345, 45, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.label_31 = QtWidgets.QLabel(self.groupBox)
        self.label_31.setGeometry(QtCore.QRect(175, 15, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.label_34 = QtWidgets.QLabel(self.groupBox)
        self.label_34.setGeometry(QtCore.QRect(260, 15, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")
        self.label_32 = QtWidgets.QLabel(self.groupBox)
        self.label_32.setGeometry(QtCore.QRect(5, 15, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.sqm = QtWidgets.QLineEdit(self.groupBox)
        self.sqm.setEnabled(False)
        self.sqm.setGeometry(QtCore.QRect(345, 30, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.sqm.setFont(font)
        self.sqm.setMouseTracking(False)
        self.sqm.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sqm.setAcceptDrops(False)
        self.sqm.setText("")
        self.sqm.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sqm.setReadOnly(True)
        self.sqm.setObjectName("sqm")
        self.label_36 = QtWidgets.QLabel(self.groupBox)
        self.label_36.setGeometry(QtCore.QRect(305, 45, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.dec = QtWidgets.QLineEdit(self.groupBox)
        self.dec.setEnabled(False)
        self.dec.setGeometry(QtCore.QRect(90, 60, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.dec.setFont(font)
        self.dec.setMouseTracking(False)
        self.dec.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dec.setAcceptDrops(False)
        self.dec.setText("")
        self.dec.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dec.setReadOnly(True)
        self.dec.setObjectName("dec")
        self.filter = QtWidgets.QLineEdit(self.groupBox)
        self.filter.setEnabled(False)
        self.filter.setGeometry(QtCore.QRect(260, 30, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.filter.setFont(font)
        self.filter.setMouseTracking(False)
        self.filter.setFocusPolicy(QtCore.Qt.NoFocus)
        self.filter.setAcceptDrops(False)
        self.filter.setText("")
        self.filter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.filter.setReadOnly(True)
        self.filter.setObjectName("filter")
        self.binX = QtWidgets.QLineEdit(self.groupBox)
        self.binX.setEnabled(False)
        self.binX.setGeometry(QtCore.QRect(260, 60, 36, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.binX.setFont(font)
        self.binX.setMouseTracking(False)
        self.binX.setFocusPolicy(QtCore.Qt.NoFocus)
        self.binX.setAcceptDrops(False)
        self.binX.setText("")
        self.binX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.binX.setReadOnly(True)
        self.binX.setObjectName("binX")
        self.label_29 = QtWidgets.QLabel(self.groupBox)
        self.label_29.setGeometry(QtCore.QRect(5, 45, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.label_35 = QtWidgets.QLabel(self.groupBox)
        self.label_35.setGeometry(QtCore.QRect(260, 45, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_35.setFont(font)
        self.label_35.setObjectName("label_35")
        self.label_37 = QtWidgets.QLabel(self.groupBox)
        self.label_37.setGeometry(QtCore.QRect(345, 15, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_37.setFont(font)
        self.label_37.setObjectName("label_37")
        self.label_30 = QtWidgets.QLabel(self.groupBox)
        self.label_30.setGeometry(QtCore.QRect(90, 45, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.object = QtWidgets.QLineEdit(self.groupBox)
        self.object.setEnabled(False)
        self.object.setGeometry(QtCore.QRect(5, 30, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.object.setFont(font)
        self.object.setMouseTracking(False)
        self.object.setFocusPolicy(QtCore.Qt.NoFocus)
        self.object.setAcceptDrops(False)
        self.object.setText("")
        self.object.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.object.setReadOnly(True)
        self.object.setObjectName("object")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(90, 15, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.scale = QtWidgets.QLineEdit(self.groupBox)
        self.scale.setEnabled(False)
        self.scale.setGeometry(QtCore.QRect(175, 30, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.scale.setFont(font)
        self.scale.setMouseTracking(False)
        self.scale.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scale.setAcceptDrops(False)
        self.scale.setText("")
        self.scale.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.scale.setReadOnly(True)
        self.scale.setObjectName("scale")
        self.hasCelestial = QtWidgets.QPushButton(self.groupBox)
        self.hasCelestial.setGeometry(QtCore.QRect(5, 80, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.hasCelestial.setFont(font)
        self.hasCelestial.setObjectName("hasCelestial")
        self.hasDistortion = QtWidgets.QPushButton(self.groupBox)
        self.hasDistortion.setGeometry(QtCore.QRect(90, 80, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.hasDistortion.setFont(font)
        self.hasDistortion.setObjectName("hasDistortion")
        self.label_33 = QtWidgets.QLabel(self.groupBox)
        self.label_33.setGeometry(QtCore.QRect(175, 45, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.rotation = QtWidgets.QLineEdit(self.groupBox)
        self.rotation.setEnabled(False)
        self.rotation.setGeometry(QtCore.QRect(175, 60, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.rotation.setFont(font)
        self.rotation.setMouseTracking(False)
        self.rotation.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rotation.setAcceptDrops(False)
        self.rotation.setText("")
        self.rotation.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.rotation.setReadOnly(True)
        self.rotation.setObjectName("rotation")
        self.groupBox_2 = QtWidgets.QGroupBox(ImageDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 75, 316, 41))
        self.groupBox_2.setObjectName("groupBox_2")
        self.color = QtWidgets.QComboBox(self.groupBox_2)
        self.color.setGeometry(QtCore.QRect(110, 15, 96, 22))
        self.color.setCurrentText("")
        self.color.setObjectName("color")
        self.stretch = QtWidgets.QComboBox(self.groupBox_2)
        self.stretch.setGeometry(QtCore.QRect(215, 15, 96, 22))
        self.stretch.setCurrentText("")
        self.stretch.setObjectName("stretch")
        self.zoom = QtWidgets.QComboBox(self.groupBox_2)
        self.zoom.setGeometry(QtCore.QRect(5, 15, 96, 22))
        self.zoom.setCurrentText("")
        self.zoom.setObjectName("zoom")

        self.retranslateUi(ImageDialog)
        QtCore.QMetaObject.connectSlotsByName(ImageDialog)

    def retranslateUi(self, ImageDialog):
        _translate = QtCore.QCoreApplication.translate
        ImageDialog.setWindowTitle(_translate("ImageDialog", "Imaging"))
        self.expose.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Single exposure</p></body></html>"))
        self.expose.setText(_translate("ImageDialog", "Expose 1"))
        self.solve.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Single plate solve of the actual image</p></body></html>"))
        self.solve.setText(_translate("ImageDialog", "Solve"))
        self.load.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Load a fits file and display is</span></p></body></html>"))
        self.load.setText(_translate("ImageDialog", "Load FITS"))
        self.stop.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Cancels an imaging or plate solving action or stops continous exposures</p></body></html>"))
        self.stop.setText(_translate("ImageDialog", "Stop Exp."))
        self.imageFileName.setToolTip(_translate("ImageDialog", "<html><head/><body><p>name of image which is shown</p></body></html>"))
        self.exposeN.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Continous exposures</span></p></body></html>"))
        self.exposeN.setText(_translate("ImageDialog", "Expose N"))
        self.groupBox.setTitle(_translate("ImageDialog", "FITS"))
        self.ccdTemp.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.expTime.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.binY.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.ra.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.label_38.setText(_translate("ImageDialog", "CCDTemp [°]"))
        self.label_31.setText(_translate("ImageDialog", "Scale [app]"))
        self.label_34.setText(_translate("ImageDialog", "Filter"))
        self.label_32.setText(_translate("ImageDialog", "Obj. Name"))
        self.sqm.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.label_36.setText(_translate("ImageDialog", "Bin Y"))
        self.dec.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.filter.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.binX.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.label_29.setText(_translate("ImageDialog", "RA [hrs]"))
        self.label_35.setText(_translate("ImageDialog", "Bin X"))
        self.label_37.setText(_translate("ImageDialog", "SQM [mpas]"))
        self.label_30.setText(_translate("ImageDialog", "DEC [deg]"))
        self.object.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.label.setText(_translate("ImageDialog", "ExpTime [s]"))
        self.scale.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.hasCelestial.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Cancels an imaging or plate solving action or stops continous exposures</p></body></html>"))
        self.hasCelestial.setText(_translate("ImageDialog", "WCS celest."))
        self.hasDistortion.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Cancels an imaging or plate solving action or stops continous exposures</p></body></html>"))
        self.hasDistortion.setText(_translate("ImageDialog", "distortion"))
        self.label_33.setText(_translate("ImageDialog", "Rotation [°]"))
        self.rotation.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.groupBox_2.setTitle(_translate("ImageDialog", "Image setting"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ImageDialog = QtWidgets.QWidget()
    ui = Ui_ImageDialog()
    ui.setupUi(ImageDialog)
    ImageDialog.show()
    sys.exit(app.exec_())

