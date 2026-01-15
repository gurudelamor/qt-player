from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from sin_orden.window_frameless import WindowFrameless
from sin_orden.widget_playlist import WidgetPlaylist
from sin_orden.main_player import MainPlayer
from sin_orden.dialog_files import DialogFiles


class TestVentanaFrameless(WindowFrameless):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__cnf_TestVentanaFrameless()

    def __cnf_TestVentanaFrameless(self):
        self.setWindowTitle('TestVentanaFrameless')
        self.resize(650, 480)


class TestWidgets(QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        #self.setupUi(self)
        self.__cnf_TestWidgets()

    def __cnf_TestWidgets(self):
        self.setWindowTitle('TestWidgets')
        self.vly = QVBoxLayout(self)
        self.vly.setContentsMargins(0,0,0,0)

    def test_playlist(self):
        self.resize(350, 450)
        self.wplaylist = WidgetPlaylist()
        self.vly.addWidget(self.wplaylist)

        self.wplaylist.lnBuscar.addAction(QIcon(u':/views/icons/search.svg'), QLineEdit.LeadingPosition)
        self.wplaylist.btBajar.clicked.connect(self.wplaylist.item_move_down)
        self.wplaylist.btSubir.clicked.connect(self.wplaylist.item_move_up)
        self.wplaylist.btEliminar.clicked.connect(self.wplaylist.delete_item)
        self.wplaylist.btOrdenar.clicked.connect(self.wplaylist.toggle_order_items)
        self.wplaylist.lnBuscar.textChanged.connect(self.wplaylist.model.filter_text)
        self.wplaylist.btPrimero.clicked.connect(self.wplaylist.select_first_item)
        self.wplaylist.btUltimo.clicked.connect(self.wplaylist.select_last_item)
        self.__show_data_initial() # si quieres testear coloca rutas a tus archivos en items

    def __show_data_initial(self):
        """test agregando archivos"""
        items = [
            'E:/Videos/musica/Something Else by element a440 b.mp4',
            'E:/Videos/musica/New World Order-(1080p25).mp4',
            'E:/Videos/musica/CARPENTER BRUT - LEATHER TEMPLE b.mp4',
            'E:/Videos/musica/IGORRR - VERY NOISE-b.mp4'
        ]
        for text in items:
            self.wplaylist.append(text)

    def test_dialog(self):
        self.resize(350, 250)
        self.dg = DialogFiles()
        self.btn = QPushButton('open Dialog')
        self.vly.addWidget(self.btn)
        self.btn.clicked.connect(self.show_dialog)

    def show_dialog(self):
        self.dg.show_dialog_select_files()
        # self.dg.show_dialog_select_dir()

        selected_files = self.dg.get_selected_files()
        for path in selected_files:
            print(path)
        for msg in self.dg._state:
            print(msg)


class TestMainPlayer(MainPlayer):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__cnf_TestMainPlayer()

    def __cnf_TestMainPlayer(self):
        self.resize(1000, 650)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # TEST VENTANA FRAMELESS
    # mv = TestVentanaFrameless()

    # TEST OTROS WIDGETS
    # mv = TestWidgets()

    # TEST PLAYLIST
    # mv.test_playlist()

    # TEST MAINPLAYER
    mv = TestMainPlayer()

    # TEST DIALOG FILES
    # mv.test_dialog()

    
    mv.show()
    sys.exit(app.exec())
    

    