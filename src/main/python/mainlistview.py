from PySide2.QtCore import Qt, QSize, QAbstractListModel
from PySide2.QtWidgets import QListView, QSizePolicy

class MainList(QListView):
    def __init__(self, *args, data=None, **kwargs):
        super(MainList, self).__init__(*args, **kwargs)
        self._data = data or []

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.MinimumExpanding
        )

    def sizeHint(self):
        return QSize(150,120)

class ListModel(QAbstractListModel):
    def __init__(self, data=None, parent=None):
        super(ListModel, self).__init__(parent)
        self._data = data or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            protein = self._data[index.row()]
            # print(protein.name)
            return f"{protein.name} ({len(protein.sequence)})"

    def rowCount(self, index):
        return len(self._data)
    
    def move_item_up(self, index):
        if index > 0:
            self._data.insert(index - 1, self._data.pop(index))
            self.dataChanged.emit(self.index(index - 1), self.index(index))

    def move_item_down(self, index):
        if index < len(self._data) - 1:
            self._data.insert(index + 1, self._data.pop(index))
            self.dataChanged.emit(self.index(index), self.index(index + 1))