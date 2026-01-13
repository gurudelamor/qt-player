# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_widget_playlist.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QLineEdit,
    QListView, QPushButton, QSizePolicy, QWidget)
import icons_rc

class Ui_WidgetPlaylist(object):
    def setupUi(self, WidgetPlaylist):
        if not WidgetPlaylist.objectName():
            WidgetPlaylist.setObjectName(u"WidgetPlaylist")
        WidgetPlaylist.resize(297, 525)
        self.gridLayout = QGridLayout(WidgetPlaylist)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.ltLista = QListView(WidgetPlaylist)
        self.ltLista.setObjectName(u"ltLista")
        self.ltLista.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)

        self.gridLayout.addWidget(self.ltLista, 0, 0, 1, 4)

        self.lnBuscar = QLineEdit(WidgetPlaylist)
        self.lnBuscar.setObjectName(u"lnBuscar")
        self.lnBuscar.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.lnBuscar, 1, 0, 1, 4)

        self.btPrimero = QPushButton(WidgetPlaylist)
        self.btPrimero.setObjectName(u"btPrimero")
        self.btPrimero.setMinimumSize(QSize(57, 0))
        self.btPrimero.setMaximumSize(QSize(16777215, 16777215))
        self.btPrimero.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/views/icons/skip-up.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btPrimero.setIcon(icon)
        self.btPrimero.setFlat(True)

        self.gridLayout.addWidget(self.btPrimero, 2, 0, 1, 1)

        self.btSubir = QPushButton(WidgetPlaylist)
        self.btSubir.setObjectName(u"btSubir")
        self.btSubir.setMinimumSize(QSize(57, 0))
        self.btSubir.setMaximumSize(QSize(16777215, 16777215))
        self.btSubir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/views/icons/play-up.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btSubir.setIcon(icon1)
        self.btSubir.setFlat(True)

        self.gridLayout.addWidget(self.btSubir, 2, 1, 1, 1)

        self.btBajar = QPushButton(WidgetPlaylist)
        self.btBajar.setObjectName(u"btBajar")
        self.btBajar.setMinimumSize(QSize(57, 0))
        self.btBajar.setMaximumSize(QSize(16777215, 16777215))
        self.btBajar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/views/icons/play-dow.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btBajar.setIcon(icon2)
        self.btBajar.setFlat(True)

        self.gridLayout.addWidget(self.btBajar, 2, 2, 1, 1)

        self.btUltimo = QPushButton(WidgetPlaylist)
        self.btUltimo.setObjectName(u"btUltimo")
        self.btUltimo.setMinimumSize(QSize(57, 0))
        self.btUltimo.setMaximumSize(QSize(16777215, 16777215))
        self.btUltimo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/views/icons/skip-dow.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btUltimo.setIcon(icon3)
        self.btUltimo.setIconSize(QSize(16, 16))
        self.btUltimo.setAutoRepeatDelay(299)
        self.btUltimo.setFlat(True)

        self.gridLayout.addWidget(self.btUltimo, 2, 3, 1, 1)

        self.widgetBotones = QWidget(WidgetPlaylist)
        self.widgetBotones.setObjectName(u"widgetBotones")
        self.gridBotones = QGridLayout(self.widgetBotones)
        self.gridBotones.setObjectName(u"gridBotones")
        self.gridBotones.setHorizontalSpacing(3)
        self.gridBotones.setContentsMargins(0, 0, 0, 0)
        self.btAgregar = QPushButton(self.widgetBotones)
        self.btAgregar.setObjectName(u"btAgregar")
        self.btAgregar.setMinimumSize(QSize(70, 0))
        self.btAgregar.setMaximumSize(QSize(16777215, 16777215))
        self.btAgregar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridBotones.addWidget(self.btAgregar, 0, 0, 1, 1)

        self.btEliminar = QPushButton(self.widgetBotones)
        self.btEliminar.setObjectName(u"btEliminar")
        self.btEliminar.setMinimumSize(QSize(70, 0))
        self.btEliminar.setMaximumSize(QSize(16777215, 16777215))
        self.btEliminar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridBotones.addWidget(self.btEliminar, 0, 1, 1, 1)

        self.btOrdenar = QPushButton(self.widgetBotones)
        self.btOrdenar.setObjectName(u"btOrdenar")
        self.btOrdenar.setMinimumSize(QSize(70, 0))
        self.btOrdenar.setMaximumSize(QSize(16777215, 16777215))
        self.btOrdenar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridBotones.addWidget(self.btOrdenar, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.widgetBotones, 3, 0, 1, 4)


        self.retranslateUi(WidgetPlaylist)

        QMetaObject.connectSlotsByName(WidgetPlaylist)
    # setupUi

    def retranslateUi(self, WidgetPlaylist):
        WidgetPlaylist.setWindowTitle(QCoreApplication.translate("WidgetPlaylist", u"Form", None))
        self.lnBuscar.setPlaceholderText(QCoreApplication.translate("WidgetPlaylist", u"Buscar ...", None))
        self.btPrimero.setText("")
        self.btSubir.setText("")
        self.btBajar.setText("")
        self.btUltimo.setText("")
        self.btAgregar.setText(QCoreApplication.translate("WidgetPlaylist", u"A\u00f1adir", None))
        self.btEliminar.setText(QCoreApplication.translate("WidgetPlaylist", u"Eliminar", None))
        self.btOrdenar.setText(QCoreApplication.translate("WidgetPlaylist", u"Ordenar", None))
    # retranslateUi

