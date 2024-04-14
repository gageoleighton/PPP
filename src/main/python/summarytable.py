from PySide2.QtWidgets import QTableView, QApplication
from PySide2.QtCore import Qt, QAbstractTableModel
from PySide2.QtGui import QKeySequence

class summaryTable(QTableView):
    def __init__(self, preserves, parent=None, *args, **kwargs):
        super(summaryTable, self).__init__(parent, *args, **kwargs)
        self.preserves = preserves
    
    def keyPressEvent(self, event):
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy()
        else:
            QTableView.keyPressEvent(self, event)

    def copy(self):
        selection = self.selectionModel()
        indexes = selection.selectedRows()
        if indexes:
            text = ''
            for x, index in enumerate(indexes):
                if x > 0:
                    text += '\n'
                row = index.row()
                print(self.model().columnCount(None))
                for col in range(0, self.model().columnCount(None)):
                    if col > 0:
                        text += '\t'
                    item = self.model().data(self.model().index(row, col), Qt.ItemDataRole.DisplayRole)
                    # print(item)
                    if item:
                        text += str(item)
            print(text)
            QApplication.clipboard().setText(text)

class summaryModel(QAbstractTableModel):
    def __init__(self, preserves=None, parent=None):
        super(summaryModel, self).__init__(parent)
        self.preserves = preserves
        self._data = []
        self.headers = ['Name', 'Sequence', 'pI', 'Extinction Reduced', 'Extinction Disulfide', 'Weight (KDa)', 'Aromaticity']
        # self.aacids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
        # self.headers.append(self.aacids)
        # self.setData()

    def setData(self):
        for keys in self.preserves.settings.allKeys():
            # print(self.preserves.settings.value(keys))
            pass


    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self.headers[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self.headers[section])

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            protein = self._data[index.column()]
            return protein.data[self.headers[index.row()]]

    def rowCount(self, index):
        return len(self.headers)

    def columnCount(self, index):
        if self._data:
            # print(len(self._data))
            return len(self._data)
        else:
            return 0