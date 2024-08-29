from PySide6.QtWidgets import QWidget, QLabel, QRadioButton, QHBoxLayout, QVBoxLayout
from base import preserves

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.firstLayout = QHBoxLayout()
        layout.addLayout(self.firstLayout)


        self.firstLayout.addWidget(QLabel("Use Sentry for error reporting (disabled while beta): "))

        self.sentryRadio = QRadioButton()
        self.sentryRadio.setDisabled(True)
        self.firstLayout.addWidget(self.sentryRadio)
        if preserves.settings.contains("sentry"):
            self.sentryRadio.setChecked(preserves.settings.value("sentry", type=bool))
        else:
            self.sentryRadio.setChecked(True)
            self.sentryToggled()

        self.sentryRadio.toggled.connect(self.sentryToggled)
    

    def sentryToggled(self):
        preserves.settings.setValue("sentry", self.sentryRadio.isChecked())
        print("Sentry: " + str(self.sentryRadio.isChecked()))
