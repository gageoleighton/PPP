"""
Python script using PyQt6 to display a QListView with QAbstractListModel and buttons to move list items up and down.
"""

import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes

class ListModel(QAbstractListModel):
    def __init__(self, data=[], parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()]

    def move_item_up(self, index):
        if index > 0:
            self._data.insert(index - 1, self._data.pop(index))
            self.dataChanged.emit(self.index(index - 1), self.index(index))

    def move_item_down(self, index):
        if index < len(self._data) - 1:
            self._data.insert(index + 2, self._data.pop(index))
            self.dataChanged.emit(self.index(index), self.index(index + 1))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("List with Move Buttons")
        layout = QVBoxLayout(self)

        self.list_view = QListView()
        self.list_model = ListModel(["Item 1", "Item 2", "Item 3"])
        self.list_view.setModel(self.list_model)
        layout.addWidget(self.list_view)

        move_up_button = QPushButton("Move Up")
        move_up_button.clicked.connect(self.move_up)
        layout.addWidget(move_up_button)

        move_down_button = QPushButton("Move Down")
        move_down_button.clicked.connect(self.move_down)
        layout.addWidget(move_down_button)

    def move_up(self):
        index = self.list_view.currentIndex().row()
        self.list_model.move_item_up(index)

    def move_down(self):
        index = self.list_view.currentIndex().row()
        self.list_model.move_item_down(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
