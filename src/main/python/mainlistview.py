from PySide6.QtCore import Qt, QSize, QAbstractListModel, QModelIndex
from PySide6.QtWidgets import QListView, QSizePolicy, QListWidget, QListWidgetItem


class MainList(QListView):
    def __init__(self, *args, data=None, **kwargs):
        super(MainList, self).__init__(*args, **kwargs)
        self._data = data or []

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding
        )

    def sizeHint(self):
        return QSize(150, 120)


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

    def insertRow(self, row: int, protein) -> bool:
        if row < 0 or row > len(self._data):
            return False
        self.beginInsertRows(QModelIndex(), row, row)
        self._data.insert(row, protein)
        self.endInsertRows()
        return True

    def move_item_up(self, index):
        if index > 0:
            self._data.insert(index - 1, self._data.pop(index))
            self.dataChanged.emit(self.index(index - 1), self.index(index))

    def move_item_down(self, index):
        if index < len(self._data) - 1:
            self._data.insert(index + 1, self._data.pop(index))
            self.dataChanged.emit(self.index(index), self.index(index + 1))


if __name__ == "__main__":
    from fbs_runtime.application_context.PySide2 import ApplicationContext
    from PySide2.QtWidgets import QApplication, QMainWindow
    import sys
    from biocalcs import protein

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.list = MainList()
            self.model = ListModel()
            self.list.setModel(self.model)
            self.setCentralWidget(self.list)
            ListModel.insertRow(
                self.model, len(self.model.rowCount()), protein("test", "test")
            )

    class AppContext(ApplicationContext):
        def __init__(self):
            super().__init__()

        def run(self):
            window = MainWindow()
            window.resize(500, 500)
            window.show()
            return self.app.exec_()

    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
