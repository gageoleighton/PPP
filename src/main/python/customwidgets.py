from PySide6.QtWidgets import QLineEdit, QDialog, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from base import context


class ClickableLineEdit(QLineEdit):
    clicked = Signal()  # signal when the text entry is left clicked

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # self.clicked.emit()
            self.deselect()
        else:
            super().mousePressEvent(event)


def aboutDialog():
    dlg = QDialog()
    dlg.setWindowTitle("About")
    layout = QHBoxLayout()
    textLabel = QLabel(
        "Built and maintained by Gage O. Leighton.<br>\
        Please address all questions to <a href='mailto:gageoleighton@gmail.com'>gageoleighton@gmail.com</a>."
    )
    # the <a href='https://www.niehs.nih.gov/research/atniehs/labs/gisbl/pi/nmr'>Mueller group at NIEHS</a>.<br>\
    #     Originally developed by 
    logo_path = context.get_resource("NIHLogo.png")
    logo = QPixmap(logo_path)
    logoLabel = QLabel()
    logoLabel.setPixmap(logo)
    # layout.addWidget(logoLabel)
    textLabel.setOpenExternalLinks(True)
    layout.addWidget(textLabel)
    dlg.setLayout(layout)
    dlg.exec()


if __name__ == "__main__":
    import sys
    from PySide2 import QtWidgets

    MainWindow = QtWidgets.QMainWindow()
    dlg = aboutDialog()
    MainWindow.setCentralWidget(dlg)
    MainWindow.show()
    sys.exit(context.app.exec_())
