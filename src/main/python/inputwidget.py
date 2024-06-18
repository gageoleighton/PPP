from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QTableWidget,
)
from customwidgets import ClickableLineEdit
from proteinmodel import ProteinModel
from biocalcs import *


class inputWidget(QWidget):
    def __init__(self, preserves):
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

        self.protein = protein(self.proteinName.text(), self.sequenceEdit.text())

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
