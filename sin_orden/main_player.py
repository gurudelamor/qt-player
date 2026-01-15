from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLineEdit, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from sin_orden.window_frameless import WindowFrameless
from sin_orden.widget_body import WidgetBody
from sin_orden.widget_info import WidgetInfo
from sin_orden.widget_playlist import  WidgetPlaylist
from sin_orden.widget_player import WidgetPlayer
from sin_orden.widget_control import WidgetControl
from sin_orden.dialog_files import DialogFiles


class MainPlayer(WindowFrameless):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__cnf_MainPlayer()

    def __cnf_MainPlayer(self):
        self.wbody = WidgetBody()
        self.winfo = WidgetInfo()
        self.winfo.setHeight(5)
        self.vly_content.addWidget(self.wbody)
        self.vly_content.addWidget(self.winfo)

        self.wplaylist = WidgetPlaylist()
        self.wbody.vly_playlist.addWidget(self.wplaylist)
        self.wplayer = WidgetPlayer()
        self.wbody.vly_player.addWidget(self.wplayer.getWidget())
        self._hotkeysPlayer()
        self.wbody.splitter.setSizes([300, 800])
        self.wbody.splitter.setStretchFactor(0, 1)
        self.wbody.splitter.setStretchFactor(1, 3)

        self.wcontrol = WidgetControl()
        self.vly_content.addWidget(self.wcontrol)
        self.vly_content.setStretch(0, 10)
        self.vly_content.setStretch(2, 1)
        self.wcontrol.btArchivo.clicked.connect(self.showDialogFiles)
        self.wcontrol.btCarpeta.clicked.connect(self.showDialogDir)


    def _hotkeysPlayer(self):
        self.hk_toggle_logo = QShortcut(QKeySequence("t"), self)
        self.hk_toggle_logo.activated.connect(self.wbody.toggleLogo)
        self.hk_toggle_info = QShortcut(QKeySequence("y"), self)
        self.hk_toggle_info.activated.connect(self.toggleInfo)

    def toggleInfo(self):
        b = not self.winfo.isHidden()
        self.winfo.setHidden(b)

    def showInfo(self, show:bool=True):
        self.winfo.setHidden(show)

    def _dialogSelect(self, dir:bool=False):
        dg = DialogFiles()
        try:
            if dir:dg.show_dialog_select_dir()
            else:dg.show_dialog_select_files()

            selected = dg.get_selected_files()
            if selected:
                self.wplaylist.set_paths(selected)
        except Exception as e:
            self.winfo.error('Dialog Files', e)
        finally:
            for msg in dg._state:
                self.winfo.msg_n(msg, num=6, br=True)

    def showDialogFiles(self):
        self._dialogSelect()
    
    def showDialogDir(self):
        self._dialogSelect(dir=True)
