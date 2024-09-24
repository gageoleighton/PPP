from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QTableWidget,
    QPushButton,
    QColorDialog,
)
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt, Signal
from customwidgets import ClickableLineEdit
from proteinmodel import ProteinModel
from biocalcs import *

from base import preserves


class ColorButton(QPushButton):
    """
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).
    """

    colorChanged = Signal(object)

    def __init__(self, *args, color=None, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)

        self._color = None
        self._default = color
        self.pressed.connect(self.onColorPicker)

        # Set the initial/default state.
        self.setColor(self._default)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)

        if self._color:
            self.setStyleSheet("background-color: %s;" % self._color)
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        """
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        """
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.setColor(self._default)

        return super(ColorButton, self).mousePressEvent(e)


class inputWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.preserves = preserves

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.nameLayout = QHBoxLayout()
        layout.addLayout(self.nameLayout)
        self.proteinNameLabel = QLabel("Protein name: ")
        self.nameLayout.addWidget(self.proteinNameLabel)
        self.proteinName = QLineEdit(
            self.preserves.settings.value("protein0", type=str)
        )
        self.nameLayout.addWidget(self.proteinName)

        self.proteinInput = QHBoxLayout()
        layout.addLayout(self.proteinInput)
        self.lengthLabel = QLabel("AA sequence: ")
        self.proteinInput.addWidget(self.lengthLabel)
        self.pILabel = QLabel()
        self.sequenceEdit = ClickableLineEdit(
            self.preserves.settings.value("sequence0", type=str)
        )
        self.proteinInput.addWidget(self.sequenceEdit)
        self.sequenceEdit.setClearButtonEnabled(True)

        self.sequenceEdit.textChanged.connect(self.update_protein_length)

        self.update_protein_length()

        # self.colorButton = ColorButton(color='#62C6F2')
        self.colorButton = ColorButton("", color="white")
        self.colorButton.setFixedSize(20, 20)
        self.proteinInput.addWidget(self.colorButton)

        self.settings = QHBoxLayout()
        layout.addLayout(self.settings)
        layout.addStretch()

        # Input view ---------------------------------------------------

        self.headers = [
            "Name",
            "Sequence",
            "pI",
            "Extinction Reduced",
            "Extinction Disulfide",
            "Weight",
            "Aromaticity",
            "Flexibility",
        ]

        self.protein = protein(
            self.proteinName.text(), self.sequenceEdit.text(), self.colorButton.color()
        )

        # self.sequenceEdit.textChanged.connect(self.calculate)
        # self.dataView.verticalHeader().setVisible(True)

    def update_protein_length(self):
        # remove spaces
        self.sequenceEdit.setText(self.sequenceEdit.text().replace(" ", ""))
        self.lengthLabel.setText("AA sequence: " + str(len(self.sequenceEdit.text())))

    # def calculate(self):
    #     self.protein = protein(self.proteinName.text(), self.sequenceEdit.text())
    #     self.proteinModel.protein = self.protein.data
    #     self.proteinModel.layoutChanged.emit()
