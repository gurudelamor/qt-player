from pathlib import Path
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtGui import QStandardItem, QStandardItemModel
from sin_orden.widget_playlist.ui_widget_playlist import Ui_WidgetPlaylist


class Model(QStandardItemModel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__cnf_Model()

    def __cnf_Model(self):
        self.ORDERED:bool = False
        self.HISTORY:list = []
        # self.ITEMS = []
        # self.INDEX = -1

        self.model_filtered = QSortFilterProxyModel()
        self.model_filtered.setSourceModel(self)
        self.model_filtered.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def filter_text(self, text:str):
        self.model_filtered.setFilterFixedString(text)


class WidgetPlaylist(QWidget, Ui_WidgetPlaylist):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.setupUi(self)
        self.__cnf_WidgetPlaylist()

    def __cnf_WidgetPlaylist(self):
        self.model = Model()
        self.model_filtered = self.model.model_filtered
        self.ltLista.setModel(self.model_filtered)
        self.lnBuscar.setPlaceholderText('Buscar:')

    def append(self, path:str):
        """agrega una nueva ruta a la playlist"""
        name = Path(path).name
        item = QStandardItem(name)
        item.setData(path, Qt.UserRole)
        item.setEditable(False)
        self.model.appendRow(item)

    def selection_step_up(self):
        """mueve la seleccion arriba"""
        current_index = self.ltLista.currentIndex()
        row = current_index.row()
        if current_index.isValid() and row > 0:
            new_index = self.model_filtered.index(row-1, 0)
            self.ltLista.setCurrentIndex(new_index)

    def selection_step_down(self):
        """mueve la seleccion abajo"""
        current_index = self.ltLista.currentIndex()
        row = current_index.row()
        if current_index.isValid() and row < self.model_filtered.rowCount()-1:
            new_index = self.model_filtered.index(row+1, 0)
            self.ltLista.setCurrentIndex(new_index)

    def _move_item(self, mod:int, condition:bool):
        """mueve el item arriba o abajo, mod=1 mueve el item 1 puesto"""
        index_lv = self.ltLista.currentIndex()
        if not index_lv.isValid():
            return

        index_model = self.model_filtered.mapToSource(index_lv)
        row = index_model.row()
        if condition:
            item = self.model.takeRow(row)
            self.model.insertRow(row+mod, item)

            new_index_model = self.model.index(row+mod, 0)
            new_index_lv = self.model_filtered.mapFromSource(new_index_model)
            self.ltLista.setCurrentIndex(new_index_lv)

    def item_move_up(self):
        """mueve el item arriba"""
        index = self.model_filtered.mapToSource(self.ltLista.currentIndex())
        cd = True if index.row() > 0 else False
        self._move_item(-1, cd)

    def item_move_down(self):
        """mueve el item abajo"""
        index = self.model_filtered.mapToSource(self.ltLista.currentIndex())
        cd = True if index.row() < self.model.rowCount()-1 else False
        self._move_item(+1, cd)

    def delete_item(self):
        """borra un item seleccionado"""
        index_lv = self.ltLista.currentIndex()
        if not index_lv.isValid():
            return

        index_model = self.model_filtered.mapToSource(index_lv)
        self.model.removeRow(index_model.row())

        if self.model.ORDERED:
            self.model.ORDERED = False

    def clear(self):
        """borra todos los items de la lista"""
        self.model.clear()
        self.model.HISTORY = []
        self.model.ORDERED = False
        
    def toggle_order_items(self):
        """ordena los items alfabeticamente y revierte al volver a presionar"""
        if self.model.ORDERED:
            self.model.clear()
            for text in self.model.HISTORY:
                item = QStandardItem(text)
                self.model.appendRow(item)
            self.model.ORDERED = False
        else:
            self.model.HISTORY = []
            for row in range(self.model.rowCount()):
                item = self.model.item(row)
                self.model.HISTORY.append(item.text())

            history = self.model.HISTORY.copy()
            history.sort()

            self.model.clear()
            for text in history:
                item = QStandardItem(text)
                self.model.appendRow(item)
            self.model.ORDERED = True

    def get_path_from_row(self, row:int) -> str|None:
        """obtiene la ruta indicandole un fila"""
        item = self.model.item(row)
        if item:
            return item.data(Qt.UserRole)

    def selection_set_row(self, row:int):
        """asigna la fila seleccionada"""
        index_selected = self.model.index(row, 0)
        if index_selected.isValid():
            index_model = self.model_filtered.mapFromSource(index_selected)
            self.ltLista.setCurrentIndex(index_model)
        
    def rowCount(self) -> int:
        """retoran la cantidad de elementos que hay (int)"""
        return self.model.rowCount()
        
    def select_last_item(self):
        """selecciona el ultimo item"""
        row = self.rowCount() -1
        self.selection_set_row(row)

    def select_first_item(self):
        """selecciona el primer item"""
        self.selection_set_row(0)

    def set_paths(self, paths:list):
        """asigna una lista de archivos"""
        for path in paths:
            self.append(path)


        
