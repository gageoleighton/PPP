from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout

class Concentration(QWidget):
    def __init__(self):
        super().__init__()
        self.extinctions = []
        self.mass = []

        layout = QHBoxLayout()
        self.setLayout(layout)

        leftLayout = QVBoxLayout()
        layout.addLayout(leftLayout)

        self.inputLayout = QHBoxLayout()
        self.inputLabel = QLabel("Absorbance 280 nm:")
        self.inputLayout.addWidget(self.inputLabel)
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
            self.outputRLabel.setText("Concentration reduced (uM): " + str(round(1000000 * float(self.input.text())/self.extinctions[0], 2)))
            self.outputCLabel.setText("Concentration disulfide (uM): " + str(round(1000000 * float(self.input.text())/self.extinctions[1],2)))

            self.outputRLabelmg.setText("Concentration reduced (mg/mL): " + str(round(self.mass * float(self.input.text())/self.extinctions[0],2)))
            self.outputCLabelmg.setText("Concentration disulfide (mg/mL): " + str(round(self.mass * float(self.input.text())/self.extinctions[1],2)))