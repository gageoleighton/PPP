"Application Corrupt run xattr -cr /path/to/application.app"

from base import context, preserves
from fbs_runtime import PUBLIC_SETTINGS

import sys, os

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QListView,
    QTableWidget,
    QTabWidget,
    QTableWidgetItem,
    QFileDialog,
    QSizePolicy,
    QMessageBox,
    QSplitter,
)
from PySide6.QtGui import QIcon, QCloseEvent, QAction
from PySide6.QtCore import Qt, QEvent, QItemSelectionModel

import qdarktheme

from customtitlebar import CustomTitleBar

from mainWidget import MainWidget
from inputwidget import inputWidget
from filterwidget import FilterWidget

# from maintreeview import MainTreeView, TreeModel, Node
from summarytable import summaryTable, summaryModel
from aatab import aaTab
from concentration import Concentration

from mainlistview import MainList, ListModel
from biocalcs import *

from Bio import SeqIO

from customwidgets import *


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    """
    Main Window Class
    """

    def __init__(self):
        super().__init__()

        # Set base color to this:
        # self.setStyleSheet("background-color: black; border-radius: 10px;")

        # Menu bar ---------------------------------------------------

        menu = self.menuBar()
        # menu.setNativeMenuBar(False)

        file_menu = menu.addMenu("&File")

        import_action = QAction("&Import", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self.import_data)

        export_action = QAction("&Export", self)
        export_action.setShortcut("Ctrl+E")
        # export_action.setDisabled(True)
        export_action.triggered.connect(self.export_data)
        # export_action.triggered.connect(lambda: self.preserves.export_settings(self))

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(lambda: preserves.save_settings(self))

        delete_save_action = QAction("&Delete Save", self)
        delete_save_action.setShortcut("Ctrl+D")
        delete_save_action.triggered.connect(preserves.delete_settings)

        file_menu.addActions(
            [import_action, export_action, save_action, delete_save_action]
        )

        help_menu = menu.addMenu("&Help")
        about_action = QAction("&About...", self)
        about_action.triggered.connect(aboutDialog)
        help_menu.addActions([about_action])

        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)


    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        if preserves.settings.value("proteinCount", type=int) != len(
            self.mainWidget.listWidget.listModel._data
        ):
            dlg = QMessageBox()
            dlg.setWindowTitle("Quit")
            dlg.setText("Save before quitting?")
            dlg.setIcon(QMessageBox.Icon.Question)
            dlg.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            dlg.setDefaultButton(QMessageBox.StandardButton.No)
            ret = dlg.exec()
            if ret == QMessageBox.StandardButton.Yes:
                preserves.save_settings(self)
                event.accept()
            else:
                event.accept()
        else:
            event.accept()

    def export_data(self) -> None:
        # dialog for saving file
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Export data", "", "Fasta Files (*.fasta)"
        )
        if fileName:
            with open(fileName, "w") as f:
                data = self.mainWidget.listModel._data
                for item in data:
                    f.write(f">{item.name}\n{item.sequence}\n")

    def import_data(self) -> None:
        # dialog for loading file
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Import data", "", "Fasta Files (*.fasta)"
        )
        if fileName:
            with open(fileName, "r") as f:
                for line in f:
                    if line[0] == ">":
                        name = line[1:].strip()
                        sequence = ""
                    else:
                        sequence += line.strip()
                        self.listModel._data.append(protein(name, sequence))
                self.listModel.layoutChanged.emit()


def run():
    """
    Runs the application."""
    window = MainWindow()
    window.setWindowTitle(
        f'{PUBLIC_SETTINGS["app_name"]} - Version: {PUBLIC_SETTINGS["version"]}'
    )
    # self.app.setWindowIcon(QIcon(self.get_resource("close.svg")))
    window.resize(500, 500)
    window.show()
    # qdarktheme.setup_theme("auto")
    qdarktheme.setup_theme("auto", corner_shape="rounded")
    return context.app.exec()


if __name__ == "__main__":
    exit_code = run()
    sys.exit(exit_code)
