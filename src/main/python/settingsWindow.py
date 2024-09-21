from PySide6.QtWidgets import QWidget, QLabel, QRadioButton, QHBoxLayout, QVBoxLayout
from base import preserves

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.sentryLayout = QHBoxLayout()
        layout.addLayout(self.sentryLayout)


        self.sentryLayout.addWidget(QLabel("Use Sentry for error reporting (disabled while beta): "))

        self.sentryRadio = QRadioButton()
        self.sentryRadio.setDisabled(True)
        self.sentryLayout.addWidget(self.sentryRadio)
        self.sentryRadio.setChecked(True)
