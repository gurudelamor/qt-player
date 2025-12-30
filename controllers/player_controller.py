import os
from PySide6.QtWidgets import QMainWindow, QApplication, QLineEdit, QFileDialog, QMessageBox, QListView, QAbstractItemView, QTreeView, QLabel, QSizePolicy

from PySide6.QtCore import Qt, QSize, QPoint, QRect, QModelIndex, QDir, QTimer, QEvent

from PySide6.QtGui import QIcon, QScreen, QMouseEvent, QStandardItemModel, QStandardItem, QAbstractFileIconProvider, QPixmap, QPainter, QFont, QColor, QImage

from PySide6.QtMultimediaWidgets import QVideoWidget

from PySide6.QtMultimedia import QMediaMetaData, QMediaPlayer

# -------------------------------------------------------------------
from views.ui.qtplay import Ui_MainPlayer
from services.player_service import PlayerService


# Extensiones válidas para medios (controlador: solo filtrado de UI)
VALID_MEDIA_EXTS = (
    # Video
    ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".ts", ".webm", ".H264", ".3gp", ".mpg", ".mpeg",
    # Audio
    ".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"
) 

class PlayerController(QMainWindow, Ui_MainPlayer):
    """Controller for the main player window: UI setup, window behavior, event handling."""

    def __init__(self, parent = None):
        super(PlayerController, self).__init__(parent)

        # --- Setup de la interfaz ---
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(open('views/skins/default.qss', 'r', encoding='utf-8').read())


        # Crear el widget de video
        self.video_widget = QVideoWidget(self.frPlayer)
        self.video_widget.setObjectName("videoWidget")
        self.video_widget.hide()

        self.lbMetas.setWordWrap(True)
        self.lbMetas.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.lbMetas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.lbMetas.hide()


        self.lbLogo.setWordWrap(True)
        self.lbLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbLogo.hide()
        self.lbLogo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)



        self.gridArchivos.addWidget(self.video_widget, 0, 0, 1, 1)
        self.gridArchivos.addWidget(self.lbLogo,       0, 0, 1, 1)

        self.gridPlayer.setRowStretch(0, 100)  # área principal (widgetArchivos)
        self.gridPlayer.setRowStretch(1, 0)    # barra inferior (lbMetas)


        # --- Servicio multimedia ---
        self.player_service = PlayerService()
        self.player_service.set_video_output(self.video_widget)

        # --- Conexión de señal de índice para refrescar UI al cambiar pista 
        # self.player_service.currentIndexChanged.connect(lambda _: self._refreshDisplayForCurrent())


        # --- Estado persistente de visibilidad de la lista ---
        lista_visible = self.player_service.state_service.load("lista_visible", True, type = bool)

        # Aplicar visibilidad
        self.frLista.setVisible(lista_visible)

        # Ajustar tamaños del splitter
        if lista_visible:
        # Lista visible: dar espacio mínimo a la lista
            self.splitter.setSizes([300, max(1, self.width() - 300)])
            self.btLista.setIcon(QIcon(u":/views/icons/box-list.svg"))
        else:
        # Lista oculta: todo el ancho para el reproductor
            self.splitter.setSizes([0, max(1, self.width())])
            self.btLista.setIcon(QIcon(u":/views/icons/box-list-off.svg"))


        self.player_service.currentIndexChanged.connect(self._onTrackChanged)

        # --- Volumen ---
        volume = self.player_service.state_service.load("volume", 50, type = int)
        self.slVolumen.setRange(0, 100)
        self.slVolumen.setValue(volume)
        self._onVolumeChanged(volume)

        # --- Repeat ---
        self._syncRepeatIcon()
        # en __init__, tras self._syncRepeatIcon()
        self._syncShuffleIcon()


        # Playlist model
        self.playlist_model = QStandardItemModel(self)
        self.ltLista.setModel(self.playlist_model)
        self.ltLista.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Estados para arrastre de ventana
        self.old_pos = QPoint()
        self.dragging = False

        # Conexión de señales
        self._connectSignals()
        self._connectPlayerSignals()


        # Al final del __init__ del PlayerController, tras configurar UI y servicios:
        self._updateMediaDisplay(file_path = "", playing = False)  # Logo “Sinergia” expansivo desde el inicio


    # -------------------------------
    # Conexión de señales de la UI
    # -------------------------------
    def _connectSignals(self):
        # Reproductor
        self.btLista.clicked.connect(self._toggleListaVisible)
        self.btShuffle.clicked.connect(self._toggleShuffleMode)
        self.btRepetir.clicked.connect(self._toggleRepeatMode)
        self.btPlay.clicked.connect(self._togglePlayPause)
        self.btStop.clicked.connect(self._onStopClicked)
        self.btBack.clicked.connect(lambda: self.player_service.seek(max(0, self.player_service.position() - 5000)))
        self.btSkipBack.clicked.connect(self.player_service.previous)
        self.btForward.clicked.connect(lambda: self.player_service.seek(self.player_service.position() + 5000))
        self.btSkipForward.clicked.connect(self.player_service.next)

        # Volumen
        self.slVolumen.valueChanged.connect(self._onVolumeChanged)
        self.btVolumen.clicked.connect(self._toggleMute)

        # Ventana
        self.btPin.clicked.connect(self.btPinToggle)
        self.btMax.clicked.connect(self.btMaxMin)
        self.btSquare.clicked.connect(self.toggleFullScreen)
        self.btClose.clicked.connect(self.close)
        self.btMin.clicked.connect(lambda: self.showMinimized() if not self.isMinimized() else None)

        # Lista y carga  _onAddFolders
        self.btArchivo.clicked.connect(self._onAddFiles)
        self.btCarpeta.clicked.connect(self._onAddFolders)


        self.btEliminar.clicked.connect(self._onRemoveSelected)
        self.ltLista.doubleClicked.connect(self._onPlaySelected)

        # Búsqueda
        self.lnBuscar.addAction(QIcon(u":/views/icons/search.svg"), QLineEdit.LeadingPosition)

        # Barra de tiempo
        self.slTiempo.sliderMoved.connect(self._onSeekFromSlider)

    # -------------------------------
    # Conexión de señales del QMediaPlayer
    # -------------------------------
    def _connectPlayerSignals(self):

        self.player_service.player.positionChanged.connect(self._updateTime)
        self.player_service.player.durationChanged.connect(self._updateDuration)
        self.player_service.player.playbackStateChanged.connect(self._updatePlayButtonIcon)

        # 👇 Añade esta línea aquí 
        self.player_service.player.playbackStateChanged.connect(self._onPlaybackStateChanged)

        # self.player_service.player.metaDataChanged.connect(self._updateLogoWithMeta)

        # --- NUEVAS señales para refrescar UI en más casos --- 
        p = self.player_service.player 
        # Cuando el medio está cargado/buffered 
        p.mediaStatusChanged.connect(self._onMediaStatusChanged) 
        # Cuando cambia la fuente (clic en lista, next/prev) 
        # p.sourceChanged.connect(self._onSourceChanged)

    # -------------------------------
    # Handlers de UI: playlist y archivos
    # -------------------------------

    def _onAddFiles(self):
        dialog = QFileDialog(self, "Seleccionar archivos multimedia 🎶 🎞")
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, False)

        # Abrir en raíz del sistema (C:\ en Windows ::{20D04FE0-3AEA-1069-A2D8-08002B30309D})
        # dialog.setDirectory(QDir.rootPath())
        dialog.setDirectory("::{20D04FE0-3AEA-1069-A2D8-08002B30309D}")

        filtros = (
            "Todos los medios (*.mp4 *.avi *.mkv *.mov *.mp3 *.wav *.ogg *.flac *.aac *.m4a);;"
            "Video (*.mp4 *.avi *.mkv *.mov);;"
            "Audio (*.mp3 *.wav *.ogg *.flac *.aac *.m4a)"
        )
        dialog.setNameFilter(filtros)

        if dialog.exec():
            file_paths = dialog.selectedFiles()

            for file_path in file_paths:
                # ✅ Usar la constante VALID_MEDIA_EXTS
                if file_path.lower().endswith(VALID_MEDIA_EXTS):
                    if file_path not in self.player_service.playlist:
                        self.player_service.load(file_path)
                        item = QStandardItem(os.path.basename(file_path))
                        item.setData(file_path, Qt.UserRole)
                        item.setEditable(False)
                        self.playlist_model.appendRow(item)

            if self.playlist_model.rowCount() > 0 and self.player_service.current_index == -1:
                self.ltLista.setCurrentIndex(self.playlist_model.index(0, 0))
                self.player_service.set_current_index(0)


    def _onAddFolders(self):
        dialog = QFileDialog(self, "Seleccionar carpetas de música/video 📁")
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ReadOnly, True)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)

        # Abrir en raíz del sistema (C:\ en Windows)
        # dialog.setDirectory(QDir.rootPath())
        dialog.setDirectory("::{20D04FE0-3AEA-1069-A2D8-08002B30309D}")

        # Forzar selección múltiple
        for view_type in [QListView, QTreeView]:
            view = dialog.findChild(view_type)
            if view:
                view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        if dialog.exec():
            folder_paths = dialog.selectedFiles()
            self.playlist_model.layoutAboutToBeChanged.emit()

            for folder in folder_paths:
                folder = os.path.normpath(folder)
                if os.path.isdir(folder):
                    for root, _, files in os.walk(folder):
                        for file in files:
                            if file.lower().endswith(VALID_MEDIA_EXTS):
                                full_path = os.path.normpath(os.path.join(root, file))
                                if full_path not in self.player_service.playlist:
                                    self.player_service.load(full_path)
                                    item = QStandardItem(file)
                                    item.setData(full_path, Qt.UserRole)
                                    item.setEditable(False)
                                    self.playlist_model.appendRow(item)

            self.playlist_model.layoutChanged.emit()

            if self.playlist_model.rowCount() > 0 and self.player_service.current_index == -1:
                self.ltLista.setCurrentIndex(self.playlist_model.index(0, 0))
                self.player_service.set_current_index(0)


    # def _onAddFolders(self):
    #     dialog = QFileDialog(self, "Seleccionar carpetas de música/video 📁")
    #     dialog.setFileMode(QFileDialog.FileMode.Directory)
    #     dialog.setOption(QFileDialog.Option.ReadOnly, True)
    #     dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        
    #     # Iniciar en "Este equipo"
    #     dialog.setDirectory("::{20D04FE0-3AEA-1069-A2D8-08002B30309D}") 

    #     # Forzar selección múltiple
    #     for view_type in [QListView, QTreeView]:
    #         view = dialog.findChild(view_type)
    #         if view:
    #             view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    #     if dialog.exec():
    #         folder_paths = dialog.selectedFiles()
            
    #         # Bloqueamos actualizaciones visuales para ganar velocidad
    #         self.playlist_model.layoutAboutToBeChanged.emit()
            
    #         for folder in folder_paths:
    #             # Normalizamos la ruta para evitar problemas con carpetas del sistema (Escritorio, etc.)
    #             folder = os.path.normpath(folder)
                
    #             if os.path.isdir(folder):
    #                 for root, _, files in os.walk(folder):
    #                     for file in files:
    #                         if file.lower().endswith(filtros):
    #                             full_path = os.path.normpath(os.path.join(root, file))
                                
    #                             if full_path not in self.player_service.playlist:
    #                                 # 1. Cargar en el servicio
    #                                 self.player_service.load(full_path)
                                    
    #                                 # 2. Crear ítem y añadirlo como FILA (appendRow)
    #                                 # Usamos appendRow porque es una lista vertical
    #                                 item = QStandardItem(file)
    #                                 item.setData(full_path, Qt.UserRole)
    #                                 item.setEditable(False)
    #                                 self.playlist_model.appendRow(item)

    #         # Notificamos que la UI ya puede refrescarse
    #         self.playlist_model.layoutChanged.emit()

    #         # Autoselección si es la primera carga
    #         if self.playlist_model.rowCount() > 0 and self.player_service.current_index == -1:
    #             self.ltLista.setCurrentIndex(self.playlist_model.index(0, 0))
    #             self.player_service.set_current_index(0)

    def _onRemoveSelected(self):
        index: QModelIndex = self.ltLista.currentIndex()
        if not index.isValid():
            return

        row = index.row()
        self.playlist_model.removeRow(row)

        if 0 <= row < len(self.player_service.playlist):
            del self.player_service.playlist[row]

        if self.playlist_model.rowCount() > 0:
            new_index = min(row, self.playlist_model.rowCount() - 1)
            self.ltLista.setCurrentIndex(self.playlist_model.index(new_index, 0))
            self.player_service.set_current_index(new_index)
        else:
            self.player_service.stop()
            self.player_service.current_index = -1

    def _onPlaySelected(self, index: QModelIndex):
        print(f"DEBUG: _onPlaySelected llamado con row {index.row()}")
        # Fijar índice actual según el clic
        row = index.row()
        self.player_service.set_current_index(row)

        # Obtener filepath desde el rol correcto
        item = self.playlist_model.itemFromIndex(index)
        if not item:
            return

        file_path = item.data(Qt.UserRole)  # ✅ lee desde UserRole
        if not file_path:
            return

        # --- NUEVA VALIDACIÓN: Verificar si el archivo existe ---
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Archivo no encontrado", f"El archivo '{os.path.basename(file_path)}' no se encuentra en la ruta especificada.\n\nPosiblemente fue movido o eliminado.")
            return
        # -------------------------------------------------------

        # Actualizar labels y reproducir
        self._updateTitleAndExtension(file_path)
        # --- LLAMADA ADICIONAL: Ajustar visibilidad de widgets (logo/video/cover) ---
        # self._updateMediaDisplay(file_path)
        self._updateMediaDisplay(file_path, playing = True)
        # ----------------------------------------------------------------------------
        self.player_service.play()

    def _onTrackChanged(self, new_index: int):
        """
        Maneja el cambio de pista en la playlist.
        Solo actualiza los labels de título y extensión,
        sin modificar la visibilidad de logo/video/cover.
        """
        print(f"DEBUG: _onTrackChanged - rowCount: {self.playlist_model.rowCount()}, new_index: {new_index}")
        if 0 <= new_index < self.playlist_model.rowCount():
            item = self.playlist_model.item(new_index)
            print(f"DEBUG: _onTrackChanged - item: {item}")
            if item:
                file_path = item.data(Qt.UserRole)
                print(f"DEBUG: _onTrackChanged - file_path: {file_path}")
                if file_path:
                    # ✅ Solo actualizar labels
                    self._updateTitleAndExtension(file_path)
                else:
                    print("DEBUG: _onTrackChanged - file_path es None o vacío")
            else:
                print("DEBUG: _onTrackChanged - item es None")
        else:
            print("DEBUG: _onTrackChanged - index fuera de rango")

    def _updateMediaDisplay(self, file_path: str, playing: bool = False):
        # Estado inicial o sin ruta válida → logo genérico
        if not file_path:
            self.video_widget.hide()
            self.lbLogo.setMaximumSize(16777215, 16777215)
            self.lbLogo.setPixmap(QPixmap())
            self.lbLogo.setText("Sinergia 🎞")
            self.lbLogo.show()
            self.lbMetas.hide()
            return

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in tuple(x.lower() for x in VALID_MEDIA_EXTS):
            self.video_widget.hide()
            self.lbLogo.setMaximumSize(16777215, 16777215)
            self.lbLogo.setPixmap(QPixmap())
            self.lbLogo.setText("Sinergia")
            self.lbLogo.show()
            self.lbMetas.hide()
            return

        # Antes de reproducir → mantener logo
        if not playing:
            self.video_widget.hide()
            self.lbLogo.setMaximumSize(16777215, 16777215)
            self.lbLogo.setPixmap(QPixmap())
            self.lbLogo.setText("Sinergia")
            self.lbLogo.show()
            self.lbMetas.hide()
            return

        # Ya reproduciendo → video o audio con/sin portada
        VIDEO_EXTS = VALID_MEDIA_EXTS[:11]
        AUDIO_EXTS = VALID_MEDIA_EXTS[11:]

        if ext in VIDEO_EXTS:
            self.lbLogo.hide()
            self.lbMetas.hide()
            self.video_widget.show()
            return

        if ext in AUDIO_EXTS:
            self.video_widget.hide()

            # Esperar a que los metadatos estén cargados
            status = self.player_service.player.mediaStatus()
            if status in (QMediaPlayer.BufferingMedia, QMediaPlayer.LoadingMedia):
                # Defer: mantener logo si aún no hay metadata confiable
                self.lbLogo.setMaximumSize(16777215, 16777215)
                self.lbLogo.setPixmap(QPixmap())
                self.lbLogo.setText("Sinergia")
                self.lbLogo.show()
                self.lbMetas.hide()
                return

            meta = self.player_service.player.metaData()
            title  = meta.stringValue(QMediaMetaData.Title) or ""
            artist = meta.stringValue(QMediaMetaData.ContributingArtist) or ""
            album  = meta.stringValue(QMediaMetaData.AlbumTitle) or ""
            year   = meta.stringValue(QMediaMetaData.Date) or ""
            lineas = [t for t in (title, artist, album) if t]
            texto  = "\n".join(lineas) if lineas else "Sinergia"

            # texto  = " — ".join([t for t in (title, artist, album, year) if t]) or "Sinergia"

            img = meta.value(QMediaMetaData.ThumbnailImage)
            if isinstance(img, QImage) and not img.isNull():
                self.lbLogo.setMaximumSize(300, 300)  # límite tipo PotPlayer
                pix = QPixmap.fromImage(img).scaled(
                    self.lbLogo.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.lbLogo.setPixmap(pix)
                self.lbLogo.setText("")
                self.lbLogo.show()
                # self.widgetArchivos.setStyleSheet(u"background-color:  #aa007f;border: 1px solid #020202;")
                # self.frPlayer.setStyleSheet(u"border: none;")
                self.lbMetas.setText(texto)
                self.lbMetas.show()
                return

            # Sin portada → logo expansivo + metadatos
            self.lbLogo.setMaximumSize(16777215, 16777215)
            self.lbLogo.setPixmap(QPixmap())
            self.lbLogo.setText("Sinergia")
            self.lbLogo.show()

            self.lbMetas.setText(texto)
            self.lbMetas.show()
            return

    def _togglePlayPause(self):
        if self.player_service.is_playing():
            self.player_service.pause()
        else:
            idx = self.player_service.current_index
            if 0 <= idx < self.playlist_model.rowCount():
                item = self.playlist_model.item(idx)
                if item:
                    file_path = item.data(Qt.UserRole)  # ✅ UserRole
                    if file_path:
                        self._updateTitleAndExtension(file_path)
            self.player_service.play()

    def _updatePlayButtonIcon(self, state):
        from PySide6.QtMultimedia import QMediaPlayer
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.btPlay.setIcon(QIcon(u":/views/icons/pause.svg"))
        else:
            self.btPlay.setIcon(QIcon(u":/views/icons/play.svg"))

    def _onPlaybackStateChanged(self, state):
        print(f"▶️ Estado de reproducción: {state}")
        idx = self.player_service.current_index
        file_path = None
        if 0 <= idx < self.playlist_model.rowCount():
            item = self.playlist_model.item(idx)
            if item:
                file_path = item.data(Qt.UserRole)

        if state == QMediaPlayer.PlaybackState.PlayingState and file_path:
            self._updateMediaDisplay(file_path, playing = True)
        elif state == QMediaPlayer.PlaybackState.StoppedState:
            self._updateMediaDisplay("", playing = False)

    def _onMediaStatusChanged(self, status):
        # Cuando los metadatos ya están disponibles, refresca si está reproduciendo audio
        if status in (QMediaPlayer.LoadedMedia, QMediaPlayer.BufferedMedia):
            idx = self.player_service.current_index
            if 0 <= idx < self.playlist_model.rowCount():
                item = self.playlist_model.item(idx)
                if item:
                    file_path = item.data(Qt.UserRole)
                    if file_path:
                        # Usa playing=True si el estado actual es PlayingState
                        playing = (self.player_service.player.playbackState() ==
                                QMediaPlayer.PlaybackState.PlayingState)
                        if playing:
                            self._updateMediaDisplay(file_path, playing = True)

    def _onStopClicked(self):
        self.player_service.stop()
        self.btPlay.setIcon(QIcon(u":/views/icons/play.svg"))
        # Reset visuales
        self.video_widget.hide()
        self.lbMetas.hide()
        self.lbLogo.show()
        self.lbTituloArchivo.setText("")
        self.lbExtension.setText("")

    def _onVolumeChanged(self, value: int):
        self.player_service.set_volume(value)
        if value == 0:
            icon = QIcon(u":/views/icons/volume-muted.svg")
        elif value <= 30:
            icon = QIcon(u":/views/icons/volume-low.svg")
        elif value <= 70:
            icon = QIcon(u":/views/icons/volume-medium.svg")
        else:
            icon = QIcon(u":/views/icons/volume-high.svg")
        self.btVolumen.setIcon(icon)

    def _toggleRepeatMode(self):
        mode = self.player_service.repeat_mode
        if mode == "none":
            self.player_service.set_repeat_mode("all")
        elif mode == "all":
            self.player_service.set_repeat_mode("one")
        else:
            self.player_service.set_repeat_mode("none")
        self._syncRepeatIcon()

    def _syncRepeatIcon(self):
        mode = self.player_service.repeat_mode
        if mode == "none":
            self.btRepetir.setIcon(QIcon(u":/views/icons/repeat-off.svg"))
        elif mode == "all":
            self.btRepetir.setIcon(QIcon(u":/views/icons/repeat.svg"))
        else:
            self.btRepetir.setIcon(QIcon(u":/views/icons/repeat-one.svg"))

    def _toggleShuffleMode(self):
        current = self.player_service.shuffle_mode
        self.player_service.set_shuffle_mode(not current)
        self._syncShuffleIcon()

    def _syncShuffleIcon(self):
        if self.player_service.shuffle_mode:
            self.btShuffle.setIcon(QIcon(u":/views/icons/shuffle-on.svg"))
        else:
            self.btShuffle.setIcon(QIcon(u":/views/icons/shuffle-off.svg"))

    def _updateTitleAndExtension(self, file_path: str):
        """
        Actualiza los labels de título y extensión a partir de la ruta del archivo.
        """
        if not file_path:
            self.lbTituloArchivo.setText("")
            self.lbExtension.setText("")
            return

        base_name = os.path.basename(file_path)       # Ej: "cancion.mp3"
        title, ext = os.path.splitext(base_name)      # ("cancion", ".mp3")

        self.lbTituloArchivo.setText(title)             # solo el título
        self.lbExtension.setText(ext.lstrip(".").upper())  # extensión sin punto, en mayúsculas

    def _toggleListaVisible(self):
        visible_actual = self.frLista.isVisible()
        nuevo_estado = not visible_actual

        # Aplicar visibilidad
        self.frLista.setVisible(nuevo_estado)

        # Ajustar tamaños del splitter
        if nuevo_estado:
            self.splitter.setSizes([300, max(1, self.width() - 300)])
            self.btLista.setIcon(QIcon(u":/views/icons/box-list.svg"))
        else:
            self.splitter.setSizes([0, max(1, self.width())])
            self.btLista.setIcon(QIcon(u":/views/icons/box-list-off.svg"))

        # Guardar estado
        self.player_service.state_service.save("lista_visible", nuevo_estado)

    # -------------------------------
    # Tiempo y seek
    # -------------------------------
    def _updateDuration(self, ms: int):
        self.slTiempo.setMaximum(ms if ms > 0 else 0)
        self.slTiempo.setValue(0)
        self._updateTime(self.player_service.position())

    def _updateTime(self, ms: int):
        self.slTiempo.blockSignals(True)
        self.slTiempo.setValue(ms)
        self.slTiempo.blockSignals(False)
        dur = self.player_service.duration()
        self.lbTiempo.setText(f"{self._format_ms(ms)} / {self._format_ms(dur)}")

    def _onSeekFromSlider(self, ms: int):
        self.player_service.seek(ms)

    @staticmethod
    def _format_ms(ms: int) -> str:
        if ms <= 0:
            return "00:00:00"
        seconds = ms // 1000
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    # -------------------------------
    # Mute
    # -------------------------------
    def _toggleMute(self):
        current = self.player_service.audio_output.isMuted()
        self.player_service.mute(not current)
        icon = QIcon(u":/views/icons/volume-muted.svg") if not current else QIcon(u":/views/icons/volume-medium.svg")
        self.btVolumen.setIcon(icon)

    # ---------------------------------------------------
    # Métodos para el movimiento de la ventana sin marco
    # ---------------------------------------------------
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.old_pos = event.globalPosition().toPoint()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            delta_pos = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta_pos)
            self.old_pos = event.globalPosition().toPoint()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    # -------------------------------
    # Métodos auxiliares de ventana
    # -------------------------------
    def centerWindow(self):
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def btMaxMin(self):
        if self.isMaximized():
            self.showNormal()
            self.btMax.setIcon(QIcon(u":/views/icons/maximize.svg"))
        else:
            self.showMaximized()
            self.btMax.setIcon(QIcon(u":/views/icons/minmax.svg"))

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def btPinToggle(self):
        is_pinned = self.testAttribute(Qt.WidgetAttribute.WA_AlwaysStackOnTop)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysStackOnTop, not is_pinned)

        if is_pinned:
            self.btPin.setIcon(QIcon(u":/views/icons/pin-b.svg"))
            self.setToolTip("Pin window (Ctrl+P)")
        else:
            self.btPin.setIcon(QIcon(u":/views/icons/pin-a.svg"))
            self.setToolTip("Unpin window (Ctrl+P)")