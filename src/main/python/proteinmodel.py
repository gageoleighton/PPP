from PySide2 import QtCore

from biocalcs import ProteinAnalysis

class ProteinModel(QtCore.QAbstractTableModel):
    def __init__(self, protein, headers=['Name', 'Sequence', 'pI', 'Extinction', 'Weight', 'Aromaticity', 'Flexibility'], parent=None):
        super(ProteinModel, self).__init__(parent)
        self.protein = protein
        self._headers = headers

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return str(self._headers[section])

            if orientation == QtCore.Qt.Orientation.Vertical:
                return str(section)

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            # Look up the key by header index.
            column = index.column()
            column_key = self._headers[column]
            return self.protein[index.row()][column_key]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self.protein)

    def columnCount(self, index):
        # The length of our headers.
        return len(self._headers)
