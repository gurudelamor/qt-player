import os
from typing import Literal
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtCore import Qt, QStandardPaths
from PySide6.QtGui import QIcon
from sin_orden.read_configs import ReadConfigs

filter_op = Literal['a', 'v', 'av']


class DialogFiles(QFileDialog):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__cnf_DialogFiles()

    def __cnf_DialogFiles(self):
        self._state = list()
        self.set_state('initial')
        self.cnf = ReadConfigs()
        self.selected_file_paths = list()
        self.INI_PATH = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)
        self.setOption(QFileDialog.Option.DontUseNativeDialog, False)       

    def load_filters(self):
        """asigna las extensiones permitidas"""
        filter_v = self.cnf.get('formats.video')        
        filter_a = self.cnf.get('formats.audio')
        all = filter_v + filter_a

        filter = \
            f'Todos los medios ({" ".join(all)});;' \
            f'Video ({" ".join(filter_v)});;' \
            f'Audio ({" ".join(filter_a)})'
        return filter

    def show_dialog_select_files(self):
        """dialogo para seleccionar archivos"""
        self.set_state('select files')
        self.setFileMode(QFileDialog.FileMode.ExistingFiles)
        self.setOption(QFileDialog.Option.ShowDirsOnly, False)
        filter = self.load_filters()
        self.selected_file_paths, _ = self.getOpenFileNames(
            self, 'Selecciona uno o mas archivos',
            self.INI_PATH,
            filter
        )

    def get_selected_files(self) -> list[str]:
        """rotarna una lista con los archivos seleccionados"""
        self.set_state(f'{len(self.selected_file_paths)} archivos')
        return self.selected_file_paths
    
    def show_dialog_select_dir(self):
        """dialogo para seleccionar carpeta"""
        self.set_state('select folder')
        self.setDirectory(self.INI_PATH)
        self.setFileMode(QFileDialog.FileMode.Directory)
        self.setOption(QFileDialog.Option.ShowDirsOnly, True)

        dir = self.getExistingDirectory(
            self, 'Seleccina una carpeta',
            self.INI_PATH,
            QFileDialog.Option.ShowDirsOnly
        )
        self._apply_filter_to_dir(dir)

    def _filter_allowed(self, mode:Literal['a', 'v', 'av']='av') -> list[str]:
        """retorna una lista archivos media"""
        allowed = list()
        filter_v = self.cnf.get('formats.video')        
        filter_a = self.cnf.get('formats.audio')
        all = filter_v + filter_a
        match mode:
            case 'v':allowed = filter_v
            case 'a':allowed = filter_a
            case 'av':allowed = all
            case _:allowed = all
        return allowed
    
    def _apply_filter_to_dir(self, dir:str, mode:filter_op='av') -> list[str]:
        """aplica filtro a los archivos del directorio,
        a:audio, v:video, av:audio y video
        """
        allowed = self._filter_allowed(mode)
        self.set_state(f'allowed [{mode}]: {allowed}')
        self.selected_file_paths = []
        try:
            with os.scandir(dir) as elements:
                for element in elements:
                    if element.is_file():
                        _, ext = os.path.splitext(element.name)
                        if f'*{ext.lower()}' in allowed:
                            self.selected_file_paths.append(element.path)
        except OSError as e:
            self.set_state(f'ERROR: {e}')

    def get_state(self) -> str:
        return self._state[-1]
    
    def set_state(self, text:str):
        self._state.append(f'[DialogFiles] {text}')
