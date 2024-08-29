from PySide6.QtWidgets import QStatusBar
from PySide6.QtCore import QTimer
import asyncio

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.showMessage("Ready")
        self.timer = QTimer()
        self.timer.timeout.connect(self.reset_message)
    
    def set_message(self, message):
        self.showMessage(message)
        if message == "Coppied!":
            self.timer.start(3000)
    
    def reset_message(self):
        if self.currentMessage() == "Coppied!":
            self.set_message("Ready")
