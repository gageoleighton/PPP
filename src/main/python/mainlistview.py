from PySide6.QtCore import Qt, QSize, QAbstractListModel, QModelIndex
from PySide6.QtWidgets import QListView, QSizePolicy, QMenu, QColorDialog, QInputDialog
from PySide6.QtGui import QColor, QAction


class MainList(QListView):
    def __init__(self, *args, data=None, **kwargs):
        super(MainList, self).__init__(*args, **kwargs)
        self._data = data or []

        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )

        self.setSelectionMode(QListView.SelectionMode.ExtendedSelection)
        self.setDragDropMode(QListView.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.customContextMenuRequested.connect(self.open_menu)

    def sizeHint(self):
        return QSize(150, 120)
    
    def open_menu(self, point):
        menu = QMenu(self)
        move_up_action = QAction("Move Up", self)
        move_up_action.triggered.connect(lambda: self.model().move_item_up(self.currentIndex().row()))
        move_down_action = QAction("Move Down", self)
        move_down_action.triggered.connect(lambda: self.model().move_item_down(self.currentIndex().row()))
        menu.addAction(move_up_action)
        menu.addAction(move_down_action)
        select_color = QAction("Color...", self)
        select_color.triggered.connect(self.update_colors)
        menu.addAction(select_color)
        rename_action = QAction("Rename...", self)
        rename_action.triggered.connect(self.rename_item)
        menu.addAction(rename_action)
        menu.exec_(self.viewport().mapToGlobal(point))
    
    def update_colors(self):
        self.model().set_color(indexes=self.selectedIndexes())
        self.clearSelection()

    def rename_item(self):
        dlg = QInputDialog()
        dlg.setWindowTitle("Rename Item")
        dlg.setLabelText("Enter new name:")
        # dlg.setTextEchoMode(QInputDialog.Mode.Normal)
        dlg.setTextValue(self.model().data(self.currentIndex(), Qt.ItemDataRole.EditRole))
        if dlg.exec_():
            new_name = dlg.textValue()
            self.model().rename_item(self.currentIndex().row(), new_name)
    

class ListModel(QAbstractListModel):
    def __init__(self, data=None, parent=None):
        super(ListModel, self).__init__(parent)
        self._data = data or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            protein = self._data[index.row()]
            # print(protein.name)
            return f"{protein.name} ({len(protein.sequence)})"
        if role == Qt.ItemDataRole.BackgroundRole:
            color = self._data[index.row()].color
            return QColor(color)
        if role == Qt.ItemDataRole.ForegroundRole:
            if self._data[index.row()].color == "white":
                return Qt.GlobalColor.black
            else:
                color = list(QColor(self._data[index.row()].color).getHsv())
                color[0] = (color[0]+180) % 360
                return QColor.fromHsv(color[0], color[1], color[2], color[3])
        if role == Qt.ItemDataRole.EditRole:
            return self._data[index.row()].name

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
    
    def supportedDropActions(self):
        return Qt.DropAction.CopyAction | Qt.DropAction.MoveAction
    
    def set_color(self, indexes):
        color = QColorDialog.getColor()
        if color.isValid():
            for index in indexes:
                self._data[index.row()].color = color.name()
                self.dataChanged.emit(self.index(index.row()), self.index(index.row()))
    
    def rename_item(self, index, new_name):
        self._data[index].name = new_name
        self.dataChanged.emit(self.index(index), self.index(index))


if __name__ == "__main__":
    from fbs_runtime.application_context.PySide2 import ApplicationContext
    from PySide6.QtWidgets import QApplication, QMainWindow
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
