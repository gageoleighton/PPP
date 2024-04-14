from PySide2.QtWidgets import QLineEdit, QDialog, QLabel, QVBoxLayout
from PySide2.QtCore import Qt, Signal

class ClickableLineEdit(QLineEdit):
    clicked = Signal() # signal when the text entry is left clicked

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: 
            # self.clicked.emit()
            self.deselect()
        else: super().mousePressEvent(event)

def aboutDialog(self):
        dlg = QDialog()
        dlg.setWindowTitle("About")
        layout = QVBoxLayout()
        textLabel = QLabel('Build and maintained by the Mueller group.\n\
        Originally developed by Gage O. Leighton.\n\
        A product of the NIH')
        layout.addWidget(textLabel)
        dlg.setLayout(layout)
        dlg.exec()