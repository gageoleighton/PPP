from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QRadioButton,
)
import math


class Concentration(QWidget):
    def __init__(self):
        super().__init__()
        self.extinctions = []
        self.mass = []
        self.sequence = []

        layout = QHBoxLayout()
        self.setLayout(layout)

        leftLayout = QVBoxLayout()
        layout.addLayout(leftLayout)

        self.inputLayout = QHBoxLayout()
        self.inputLabel = QLabel("Absorbance @ ")
        self.inputLayout.addWidget(self.inputLabel)
        self.absorbance_205 = QRadioButton("205")
        self.absorbance_205.toggled.connect(self.calcConc)
        self.absorbance_280 = QRadioButton("280 nm")
        self.absorbance_280.setChecked(True)
        self.inputLayout.addWidget(self.absorbance_205)
        self.inputLayout.addWidget(self.absorbance_280)

        self.input = QLineEdit()
        self.inputLayout.addWidget(self.input)
        self.input.textChanged.connect(self.calcConc)

        leftLayout.addLayout(self.inputLayout)

        self.outputLayout = QVBoxLayout()
        self.outputRLabel = QLabel("Concentration reduced (uM): ")
        self.outputRLabel.setFixedHeight(30)
        self.outputCLabel = QLabel("Concentration disulfide (uM): ")
        self.outputCLabel.setFixedHeight(30)
        self.outputLayout.addWidget(self.outputRLabel)
        self.outputLayout.addWidget(self.outputCLabel)

        self.outputRLabelmg = QLabel("Concentration reduced (mg/mL): ")
        self.outputRLabelmg.setFixedHeight(30)
        self.outputCLabelmg = QLabel("Concentration disulfide (mg/mL): ")
        self.outputCLabelmg.setFixedHeight(30)
        self.outputLayout.addWidget(self.outputRLabelmg)
        self.outputLayout.addWidget(self.outputCLabelmg)

        self.outputLayout.addStretch()

        leftLayout.addLayout(self.outputLayout)

        rightLayout = QVBoxLayout()
        layout.addLayout(rightLayout)

    def calcConc(self):
        if self.input.text() == "":
            self.outputRLabel.setText("Concentration reduced (uM): ")
            self.outputCLabel.setText("Concentration disulfide (uM): ")
            self.outputRLabelmg.setText("Concentration reduced (mg/mL): ")
            self.outputCLabelmg.setText("Concentration disulfide (mg/mL): ")
        else:
            if self.absorbance_205.isChecked():
                self.calcConc205()
            elif self.absorbance_280.isChecked():
                self.calcConc280()

    def calcConc280(self):
        self.outputRLabel.setText(
            "Concentration reduced (uM): "
            + str(round(1000000 * float(self.input.text()) / self.extinctions[0], 2))
        )
        self.outputCLabel.setText(
            "Concentration disulfide (uM): "
            + str(round(1000000 * float(self.input.text()) / self.extinctions[1], 2))
        )

        self.outputRLabelmg.setText(
            "Concentration reduced (mg/mL): "
            + str(round(self.mass * float(self.input.text()) / self.extinctions[0], 2))
        )
        self.outputCLabelmg.setText(
            "Concentration disulfide (mg/mL): "
            + str(round(self.mass * float(self.input.text()) / self.extinctions[1], 2))
        )

    def calcConc205(self):
        extinction_reduced = (
            len(self.sequence) * 2780
            + self.sequence.count("W") * 20400
            + self.sequence.count("F") * 8600
            + self.sequence.count("Y") * 6080
            + self.sequence.count("H") * 5200
            + self.sequence.count("M") * 1830
            + self.sequence.count("R") * 1350
            + self.sequence.count("C") * 690
            + self.sequence.count("D") * 400
            + self.sequence.count("Q") * 400
        )
        extinction_disulfide = (
            extinction_reduced + math.floor(self.sequence.count("c") / 2) * 820
        )
        self.outputRLabel.setText(
            "Concentration reduced (uM): "
            + str(round(100000 * float(self.input.text()) / extinction_reduced, 2))
        )
        self.outputCLabel.setText(
            "Concentration disulfide (uM): "
            + str(round(100000 * float(self.input.text()) / extinction_disulfide, 2))
        )

        self.outputRLabelmg.setText(
            "Concentration reduced (mg/mL): "
            + str(round(self.mass * float(self.input.text()) / extinction_reduced, 2))
        )
        self.outputCLabelmg.setText(
            "Concentration disulfide (mg/mL): "
            + str(round(self.mass * float(self.input.text()) / extinction_disulfide, 2))
        )
