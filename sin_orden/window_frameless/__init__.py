from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QScreen, QKeySequence, QShortcut
from sin_orden.window_frameless.ui_main_window import Ui_MainWindow


class WindowFrameless(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._is_dragging = False
        self._drag_position = None

        self.btClose.clicked.connect(self.close)
        self.btMin.clicked.connect(self.showMinimized)
        self.btMax.clicked.connect(self.toggleMaximizeRestore)
        self.btPin.toggled.connect(self.toggleOnTop)
        self.btSquare.clicked.connect(self.toggleFullscreen)
        self.centerWindow()
        self.hotkeysActivate()

    def mousePressEvent(self, event:QMouseEvent):
        if event.button() == Qt.LeftButton and self.widgetBarra.underMouse() and getattr(self, 'widgetBarra', None):
            self._is_dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event:QMouseEvent):
        if self._is_dragging:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event:QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            event.accept()

    def toggleMaximizeRestore(self):
        """maximizar|restaurar (alternar)"""
        if self.isMaximized():self.showNormal()
        else:self.showMaximized()

    def centerWindow(self):
        """centrar ventana"""
        screen = QApplication.primaryScreen()
        if screen:
            center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
            geo = self.frameGeometry()
            geo.moveCenter(center)
            self.move(geo.topLeft())

    def toggleFullscreen(self):
        """fullscreen (alternar)"""
        if self.isFullScreen():self.showNormal()
        else:self.showFullScreen()

    def toggleOnTop(self, onTop:bool):
        """sobre otras ventanas (alternar)"""
        self.setWindowFlag(Qt.WindowStaysOnTopHint, onTop)
        self.show()

    def hotkeysActivate(self):
        """activar atajos de teclado"""
        self.hk_close = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.hk_close.activated.connect(self.close)
