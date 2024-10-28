from PySide6.QtWidgets import QLineEdit, QDialog, QLabel, QHBoxLayout, QFileDialog
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from base import context
import pickle


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
        "Coded and developed by Gage O. Leighton.<br>\
        Please contact me with any questions or comments.<br>\
        gageoleighton@gmail.com"
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

def exportDialog(listView, only_selected=False):
    file_dialog = QFileDialog()
    file_dialog.setWindowTitle("Export data")
    file_dialog.setNameFilters(["Fasta Files (*.fasta)", "Protein Param Pro (*.P3)"])
    file_dialog.selectNameFilter("Protein Param Pro (*.P3)")
    file_dialog.setDefaultSuffix(".P3")
    file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)

    # file_dialog.exec()
    if file_dialog.exec() == QDialog.Accepted:
        fileName = file_dialog.selectedFiles()[0]
        with open(fileName, "wb") as f:
            if only_selected:
                data = [listView.model()._data[row.row()] for row in listView.selectedIndexes()]
            else:
                data = listView.model()._data
            if fileName.endswith(".P3"):
                pickle.dump(data, f)
            elif fileName.endswith(".fasta"):
                for item in data:
                    data = f">{item.name}\n{item.sequence}\n"
                    f.write(data.encode("utf-8"))

if __name__ == "__main__":
    import sys
    from PySide6 import QtWidgets

    MainWindow = QtWidgets.QMainWindow()
    dlg = aboutDialog()
    MainWindow.setCentralWidget(dlg)
    MainWindow.show()
    sys.exit(context.app.exec_())
