from PySide6.QtWidgets import QTableWidget
from PySide6.QtCore import Qt, QAbstractTableModel


class aaTab(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(aaTab, self).__init__(*args, **kwargs)
        self.headers = [
            "A",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "K",
            "L",
            "M",
            "N",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "V",
            "W",
            "Y",
        ]
        self._data = []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            protein = self._data[index.column()]
            return protein.data[self.headers[index.row()]]
