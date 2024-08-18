from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QTreeView, QSizePolicy, QMenu, QAction
from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex


class Node(object):
    def __init__(self, name="", parent=None):
        self._parent = parent
        self._name = name
        self._children = []

    def children(self):
        return self._children

    def hasChildren(self):
        return bool(self.children())

    def parent(self):
        return self._parent

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def type_info(self):
        return "NODE"

    def columnCount(self):
        return 1

    def child_count(self):
        return len(self._children)

    def add_child(self, child):
        self._children.append(child)
        child._parent = self

    def insert_child(self, position, child):
        if 0 <= position < child_count:
            self._children.insert(position, child)
            child._parent = self
            return True
        return False

    def remove_child(self, position):
        if 0 <= position < len(self._children):
            child = self._children.pop(position)
            child._parent = None
            return True
        return False

    def child(self, row):
        if 0 <= row < self.child_count():
            return self._children[row]

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)
        return -1

    def find_child_by_name(self, name):
        for child in self._children:
            if child.name() == name:
                return child
        return None

    def log(self, tab_level=-1):
        output = ""
        tab_level += 1

        for i in range(tab_level):
            output += "\t"

        output += "|____" + self._name + "\n"

        for child in self._children:
            output += child.log(tab_level)

        tab_level -= 1

        return output

    def __repr__(self):
        return self.log()


class MainTreeView(QTreeView):
    """PySide2 Tree View to display protein name and length."""

    def __init__(self, *args, data=None, **kwargs):
        super(MainTreeView, self).__init__(*args, **kwargs)
        self._data = data or []
        self.setDragDropMode(QTreeView.DragDropMode.InternalMove)
        self.setSelectionMode(QTreeView.SelectionMode.MultiSelection)

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding
        )

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        action = QAction("Add Folder", self)
        action.triggered.connect(self.add_folder)
        menu.addAction(action)
        menu.exec_(self.mapToGlobal(event.pos()))
        # return super().contextMenuEvent(event)

    def add_folder(self):
        pass


class TreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._root_node = Node()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if section == 0:
                return "Templates"
            else:
                return "Type"

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        node = parent.internalPointer() if parent.isValid() else self._root_node
        if node.children:
            return self.createIndex(row, column, node.child(row))
        else:
            return QModelIndex()

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()
        node = child.internalPointer()
        if node.row() >= 0:
            return self.createIndex(node.row(), 0, node.parent())
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        node = parent.internalPointer() if parent.isValid() else self._root_node
        return node.child_count()

    def columnCount(self, parent=QModelIndex()):
        return 1

    def hasChildren(self, parent=QModelIndex()):
        node = parent.internalPointer() if parent.isValid() else self._root_node
        return node.hasChildren()

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if index.isValid() and role in (
            Qt.DisplayRole,
            Qt.EditRole,
        ):
            node = index.internalPointer()
            print(node)
            return node.name()

    def setData(self, index, value, role=Qt.EditRole):
        if role in (Qt.EditRole,):
            node = index.internalPointer()
            node.set_name(value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index: QModelIndex):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def indexFromItem(self, it):
        root_index = QModelIndex()
        if isinstance(it, Node):
            parents = []
            while it is not self._root_node:
                parents.append(it)
                it = it.parent()
            root = self._root_node
            for parent in reversed(parents):
                root = root.find_child_by_name(parent.name())
                root_index = self.index(root.row(), 0, root_index)
        return root_index

    def item_from_path(self, path, sep):
        depth = path.split(sep)
        root = self._root_node
        for d in depth:
            root = root.find_child_by_name(d)
            if root is None:
                return None
        return root

    def appendRow(self, item, parent=None):
        self.appendRows([item], parent)

    def appendRows(self, items, parent=None):
        if isinstance(items, list):
            ix = self.indexFromItem(parent)
            self.insertRows(self.rowCount(ix), items, parent)

    def insertRows(self, position, items, parent=None):
        parent_index = self.indexFromItem(parent)
        self.beginInsertRows(parent_index, position, position + len(items) - 1)
        if parent is None:
            parent = self._root_node
        for item in items:
            parent.add_child(item)
        self.endInsertRows()


if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import (
        QApplication,
        QMainWindow,
        QTreeWidget,
        QTreeWidgetItem,
        QInputDialog,
    )
    from PySide2.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sortable QTreeWidget")
        self.setGeometry(100, 100, 400, 300)

        # Create QTreeWidget
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(["Items"])
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDragDropMode(QTreeWidget.InternalMove)
        self.tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.setCentralWidget(self.tree)

        # Add context menu
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_menu)

        # Add some items
        for i in range(5):
            item = QTreeWidgetItem(self.tree, [f"Item {i+1}"])
            for j in range(3):
                child = QTreeWidgetItem(item, [f"Subitem {i+1}.{j+1}"])

        self.tree.expandAll()

    def open_menu(self, position):
        indexes = self.tree.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu()
        rename_action = QAction("Rename...", self)
        rename_action.triggered.connect(self.rename_item)

        menu.exec_(self.tree.viewport().mapToGlobal(position))

    def rename_item(self):
        item = self.tree.currentItem()
        if item:
            new_name, ok = QInputDialog.getText(
                self, "Rename Item", "Enter a new name:", text=item.text(0)
            )
            if ok and new_name:
                item.setText(0, new_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
