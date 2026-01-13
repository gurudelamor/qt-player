# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(951, 644)
        font = QFont()
        font.setFamilies([u"Hack"])
        font.setPointSize(14)
        font.setItalic(True)
        MainWindow.setFont(font)
        self.widgetCentral = QWidget(MainWindow)
        self.widgetCentral.setObjectName(u"widgetCentral")
        self.gridCentral = QGridLayout(self.widgetCentral)
        self.gridCentral.setObjectName(u"gridCentral")
        self.frContent = QFrame(self.widgetCentral)
        self.frContent.setObjectName(u"frContent")
        self.frContent.setFrameShape(QFrame.Shape.StyledPanel)
        self.frContent.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frContent)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.vly_content = QVBoxLayout()
        self.vly_content.setObjectName(u"vly_content")

        self.verticalLayout_2.addLayout(self.vly_content)


        self.gridCentral.addWidget(self.frContent, 1, 0, 1, 1)

        self.widgetBarra = QWidget(self.widgetCentral)
        self.widgetBarra.setObjectName(u"widgetBarra")
        self.widgetBarra.setMinimumSize(QSize(0, 40))
        self.widgetBarra.setMaximumSize(QSize(16777215, 40))
        self.widgetBarra.setStyleSheet(u"")
        self.gridBarra = QGridLayout(self.widgetBarra)
        self.gridBarra.setObjectName(u"gridBarra")
        self.gridBarra.setContentsMargins(0, 0, 0, 0)
        self.lbTitulo = QLabel(self.widgetBarra)
        self.lbTitulo.setObjectName(u"lbTitulo")
        self.lbTitulo.setMinimumSize(QSize(120, 0))
        self.lbTitulo.setMaximumSize(QSize(120, 16777215))
        self.lbTitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridBarra.addWidget(self.lbTitulo, 0, 0, 1, 1)

        self.btMenu = QPushButton(self.widgetBarra)
        self.btMenu.setObjectName(u"btMenu")
        self.btMenu.setMinimumSize(QSize(35, 0))
        self.btMenu.setMaximumSize(QSize(35, 16777215))
        icon = QIcon()
        icon.addFile(u":/views/icons/right-arrow.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btMenu.setIcon(icon)
        self.btMenu.setFlat(True)

        self.gridBarra.addWidget(self.btMenu, 0, 1, 1, 1)

        self.lbTituloArchivo = QLabel(self.widgetBarra)
        self.lbTituloArchivo.setObjectName(u"lbTituloArchivo")
        self.lbTituloArchivo.setIndent(14)

        self.gridBarra.addWidget(self.lbTituloArchivo, 0, 2, 1, 1)

        self.lbExtension = QLabel(self.widgetBarra)
        self.lbExtension.setObjectName(u"lbExtension")
        self.lbExtension.setMinimumSize(QSize(70, 0))
        self.lbExtension.setMaximumSize(QSize(70, 16777215))
        self.lbExtension.setTextFormat(Qt.TextFormat.RichText)
        self.lbExtension.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbExtension.setWordWrap(False)
        self.lbExtension.setMargin(0)
        self.lbExtension.setIndent(0)

        self.gridBarra.addWidget(self.lbExtension, 0, 3, 1, 1)

        self.btPin = QPushButton(self.widgetBarra)
        self.btPin.setObjectName(u"btPin")
        self.btPin.setMinimumSize(QSize(37, 37))
        self.btPin.setMaximumSize(QSize(37, 37))
        self.btPin.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/views/icons/pin-a.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btPin.setIcon(icon1)
        self.btPin.setIconSize(QSize(25, 25))
        self.btPin.setCheckable(True)
        self.btPin.setFlat(True)

        self.gridBarra.addWidget(self.btPin, 0, 4, 1, 1)

        self.btMin = QPushButton(self.widgetBarra)
        self.btMin.setObjectName(u"btMin")
        self.btMin.setMinimumSize(QSize(37, 37))
        self.btMin.setMaximumSize(QSize(37, 37))
        self.btMin.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/views/icons/minimize.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btMin.setIcon(icon2)
        self.btMin.setIconSize(QSize(25, 25))
        self.btMin.setFlat(True)

        self.gridBarra.addWidget(self.btMin, 0, 5, 1, 1)

        self.btMax = QPushButton(self.widgetBarra)
        self.btMax.setObjectName(u"btMax")
        self.btMax.setMinimumSize(QSize(37, 37))
        self.btMax.setMaximumSize(QSize(37, 37))
        self.btMax.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/views/icons/maximize.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btMax.setIcon(icon3)
        self.btMax.setIconSize(QSize(25, 25))
        self.btMax.setCheckable(True)
        self.btMax.setFlat(True)

        self.gridBarra.addWidget(self.btMax, 0, 6, 1, 1)

        self.btSquare = QPushButton(self.widgetBarra)
        self.btSquare.setObjectName(u"btSquare")
        self.btSquare.setMinimumSize(QSize(37, 37))
        self.btSquare.setMaximumSize(QSize(37, 37))
        self.btSquare.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/views/icons/square.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btSquare.setIcon(icon4)
        self.btSquare.setIconSize(QSize(25, 25))
        self.btSquare.setCheckable(True)
        self.btSquare.setFlat(True)

        self.gridBarra.addWidget(self.btSquare, 0, 7, 1, 1)

        self.btClose = QPushButton(self.widgetBarra)
        self.btClose.setObjectName(u"btClose")
        self.btClose.setMinimumSize(QSize(37, 37))
        self.btClose.setMaximumSize(QSize(37, 37))
        self.btClose.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon5 = QIcon()
        icon5.addFile(u":/views/icons/close.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btClose.setIcon(icon5)
        self.btClose.setIconSize(QSize(25, 25))
        self.btClose.setFlat(True)

        self.gridBarra.addWidget(self.btClose, 0, 8, 1, 1)

        self.btMin.raise_()
        self.btClose.raise_()
        self.btPin.raise_()
        self.btMax.raise_()
        self.lbTitulo.raise_()
        self.lbExtension.raise_()
        self.lbTituloArchivo.raise_()
        self.btSquare.raise_()
        self.btMenu.raise_()

        self.gridCentral.addWidget(self.widgetBarra, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.widgetCentral)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lbTitulo.setText(QCoreApplication.translate("MainWindow", u"Sinergia", None))
        self.lbTituloArchivo.setText("")
        self.lbExtension.setText("")
        self.btPin.setText("")
        self.btMin.setText("")
        self.btMax.setText("")
        self.btSquare.setText("")
        self.btClose.setText("")
    # retranslateUi

