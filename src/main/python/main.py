"Application Corrupt run xattr -cr /path/to/application.app"

from base import context, preserves
from fbs_runtime import PUBLIC_SETTINGS

import sys, os, requests, webbrowser, pickle

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QListView,
    QTabWidget,
    QTableWidgetItem,
    QFileDialog,
    QSizePolicy,
    QMessageBox,
    QSplitter,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

import qdarktheme

# from customtitlebar import CustomTitleBar

from inputwidget import inputWidget
from filterwidget import FilterWidget
from settingsWindow import SettingsWindow

# from maintreeview import MainTreeView, TreeModel, Node
from summarytable import summaryTable, summaryModel
from aatab import aaTab
from concentration import Concentration

from statusbar import StatusBar

from mainlistview import MainList, ListModel
from biocalcs import *

# from Bio import SeqIO

from customwidgets import *


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    """
    Main Window Class
    """

    def __init__(self):
        super().__init__()
        # self.preserves = Perseverance()
        # self.proteinModel = ProteinModel(self.preserves.return_last_settings())

        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.setStyleSheet("background-color: black; border-radius: 10px;")

        # self.title_bar = CustomTitleBar(self)

        # Menu bar ---------------------------------------------------

        # self.setWindowTitle("Protein Perseverance")

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

        delete_save_action = QAction("&Delete All...", self)
        delete_save_action.setShortcut("Ctrl+D")
        delete_save_action.triggered.connect(self.delete_all)

        settings_action = QAction("&Settings", self)
        settings_action.setShortcut("Ctrl+P")
        self.settingsWindow = SettingsWindow()
        settings_action.triggered.connect(self.settingsWindow.show)

        check_updates_action = QAction("&Check for updates", self)
        check_updates_action.setShortcut("Ctrl+U")
        check_updates_action.triggered.connect(self.check_for_updates)

        # exit_action = QAction(" E&xit", self)
        # exit_action.setShortcut("Ctrl+Q")
        # exit_action.triggered.connect(lambda: self.closeEvent(QCloseEvent()))

        file_menu.addActions(
            [
                import_action,
                export_action,
                save_action,
                delete_save_action,
                settings_action,
            ]
        )

        help_menu = menu.addMenu("&Help")
        about_action = QAction("&About...", self)
        about_action.triggered.connect(aboutDialog)
        help_menu.addActions([about_action, check_updates_action])

        # Main widget ---------------------------------------------------

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainWidget.setLayout(self.mainLayout)

        self.layout = QHBoxLayout()
        # self.layout.setContentsMargins(11, 11, 0, 0)
        # self.mainLayout.addWidget(self.title_bar)
        self.mainLayout.addLayout(self.layout)

        # self.bottomBar = QWidget()
        # self.bottomBarLayout = QHBoxLayout()
        # self.bottomBar.setLayout(self.bottomBarLayout)

        # self.windowScaleButton = QPushButton("#")
        # self.windowScaleButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # self.windowScaleButton.setCursor(Qt.SizeFDiagCursor)
        # self.bottomBarLayout.addWidget(self.windowScaleButton)
        # self.bottomBarLayout.addStretch()
        # self.bottomBarLayout.setContentsMargins(0, 0, 0, 0)
        # self.mainLayout.addWidget(self.bottomBar, alignment=Qt.AlignRight)

        self.leftLayout = QVBoxLayout()

        self.addRemoveLayout = QHBoxLayout()

        self.addButton = QPushButton("Add")
        self.addRemoveLayout.addWidget(self.addButton)
        self.addButton.clicked.connect(self.add_item)

        self.removeButton = QPushButton("Delete")
        self.addRemoveLayout.addWidget(self.removeButton)
        self.removeButton.clicked.connect(self.delete_item)

        self.leftLayout.addLayout(self.addRemoveLayout)

        self.splitter = QSplitter()
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.leftWidget = QWidget()
        self.leftWidget.setLayout(self.leftLayout)
        self.splitter.addWidget(self.leftWidget)
        self.splitter.setCollapsible(0, False)

        # self.layout.addLayout(self.leftLayout)

        self.filterList = FilterWidget()
        self.leftLayout.addWidget(self.filterList)

        self.listWidget = MainList()
        self.leftLayout.addWidget(self.listWidget)
        # self.listWidget.selectionModel().selectionChanged.connect(self.selection_changed)
        # self.listView.clicked.connect(self.listView.clearSelection)

        self.listModel = ListModel()
        self.listWidget.setModel(self.listModel)
        self.listWidget.doubleClicked.connect(self.clear_selection)
        self.listWidget.selectionModel().selectionChanged.connect(
            self.selection_changed
        )

        self.adjustListLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.adjustListLayout)
        self.adjustUp = QPushButton("Up")
        self.adjustDown = QPushButton("Down")
        self.adjustListLayout.addWidget(self.adjustUp)
        self.adjustListLayout.addWidget(self.adjustDown)
        self.adjustUp.clicked.connect(self.move_up)
        self.adjustDown.clicked.connect(self.move_down)

        # self.treeView = MainTreeView()
        # self.treeModel = TreeModel()
        # self.treeView.setModel(self.treeModel)
        # self.leftLayout.addWidget(self.treeView)

        data = {
            "Project A": ["file_a.py", "file_a.txt", "something.xls"],
            "Project B": ["file_b.csv", "photo.jpg"],
            "Project C": [],
        }
        # self.treeView.setColumC

        # Settings -----------------------------------------------------------------------------

        self.tabWidget = QTabWidget()
        self.splitter.addWidget(self.tabWidget)
        self.layout.addWidget(self.splitter)
        # self.layout.addWidget(self.tabWidget)

        self.inputWidget = inputWidget()
        self.tabWidget.addTab(self.inputWidget, "Input")

        self.summaryTable = summaryTable()
        self.tabWidget.addTab(self.summaryTable, "Summary")
        self.summaryTable.setSelectionMode(QListView.SelectionMode.MultiSelection)
        self.summaryTable.setSelectionBehavior(QListView.SelectionBehavior.SelectRows)

        self.summaryModel = summaryModel()
        self.summaryTable.setModel(self.summaryModel)

        self.aaTab = aaTab()
        # self.tabWidget.addTab(self.aaTab, "Amino acids")
        self.aacids = [
            "A",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "K",
            "L",
            "M",
            "N",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "V",
            "W",
            "Y",
        ]
        self.aaTab.setVerticalHeaderLabels(self.aacids)

        self.concentration = Concentration()
        self.tabWidget.addTab(self.concentration, "Concentration")

        # self.proteinModel.layoutChanged.emit()
        self.statusBar = StatusBar(self)
        self.setStatusBar(self.statusBar)
        QApplication.clipboard().dataChanged.connect(
            lambda message="Coppied!": self.statusBar.set_message(message)
        )

        self.setCentralWidget(self.mainWidget)

        preserves.load_settings(self)

    def closeEvent(self, event) -> None:
        """
        Defines the behavior for the close event of the main window.
        Checks if any unsaved changes are present and prompts the user to save before quitting.
        Saves settings if the user chooses to do so.
        """
        super().closeEvent(event)
        if preserves.settings.value("proteinCount", type=int) != len(
            self.listModel._data
        ) or preserves.settings.value("needs_save", type=bool):
            self.closeDialog(event)
        else:
            event.accept()

    def closeDialog(self, event):
        dlg = QMessageBox()
        dlg.setWindowTitle("Quit")
        dlg.setText("Save before quitting?")
        dlg.setIcon(QMessageBox.Icon.Question)
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        dlg.setDefaultButton(QMessageBox.StandardButton.No)
        ret = dlg.exec()
        preserves.settings.setValue("needs_save", False)
        if ret == QMessageBox.StandardButton.Yes:
            preserves.save_settings(self)
            event.accept()
        else:
            event.accept()

    def check_for_updates(self):
        dlg = QMessageBox()

        url = "https://github.com/gageoleighton/PPP/releases/latest"
        response = requests.get(url)
        version = response.url.split("/").pop()
        print(version)
        # version = response.json()['message']
        if version == "latest" or version == "Not Found":
            self.statusBar.set_message("Could not check for updates.")
            dlg.setText("Could not check for updates.")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        else:
            if version > PUBLIC_SETTINGS["version"]:
                dlg.setStandardButtons(
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                dlg.setDefaultButton(QMessageBox.StandardButton.Yes)
                self.statusBar.set_message(
                    f"Latest version: {version}. Current version: {PUBLIC_SETTINGS['version']}"
                )
                dlg.setText(
                    f"New version available: {version}. Current version: {PUBLIC_SETTINGS['version']}\nDo you want to open a link to the latest version?"
                )
            else:
                dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
                self.statusBar.set_message(
                    f"Current version: {PUBLIC_SETTINGS['version']} is the latest."
                )
                dlg.setText(
                    f"Current version: {PUBLIC_SETTINGS['version']} is the latest."
                )
        ret = dlg.exec()
        if ret == QMessageBox.StandardButton.Yes:
            webbrowser.open(url)

    # def changeEvent(self, event) -> None:
    #     """
    #     Handles the change event for the window state.

    #     This function is called when the window state changes. It checks if the event type is a window state change event.
    #     If it is, it calls the `window_state_changed` method of the `title_bar` object with the current window state.
    #     Then, it calls the `changeEvent` method of the parent class to handle any other change events.
    #     Finally, it accepts the event.

    #     Parameters:
    #         event (QEvent): The event object representing the change event.

    #     Returns:
    #         None
    #     """

    #     if event.type() == QEvent.Type.WindowStateChange:
    #         self.title_bar.window_state_changed(self.windowState())
    #     super().changeEvent(event)
    #     event.accept()

    # def window_state_changed(self, state) -> None:
    #     """
    #     Handles the window state change event.

    #     This function is called when the window state changes. It checks if the window state is maximized.
    #     If it is, it sets the `normal_button` and `max_button` to visible.
    #     If it is not, it sets the `normal_button` and `max_button` to invisible.

    #     Parameters:
    #         state (Qt.WindowState): The current window state.

    #     Returns:
    #         None
    #     """
    #     self.title_bar.window_state_changed(state)
    #     self.normal_button.setVisible(state == Qt.WindowState.WindowMaximized)
    #     self.max_button.setVisible(state != Qt.WindowState.WindowMaximized)

    # def mousePressEvent(self, event) -> None:
    #     """
    #     Handles the mouse press event.

    #     This function is called when the mouse is pressed. It checks if the left mouse button is pressed.
    #     If it is, it sets the `initial_pos` variable to the current mouse position.
    #     Then, it calls the `mousePressEvent` method of the parent class to handle any other mouse press events.
    #     Finally, it accepts the event.

    #     Parameters:
    #         event (QMouseEvent): The mouse event object.

    #     Returns:
    #         None
    #     """
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self.initial_pos = event.pos()
    #     super().mousePressEvent(event)
    #     event.accept()

    # def mouseMoveEvent(self, event) -> None:
    #     """
    #     Handles the mouse move event.

    #     This function is called when the mouse is moved. It checks if the `initial_pos` variable is set.
    #     If it is, it calculates the difference between the current mouse position and the initial position.
    #     Then, it calls the `mouseMoveEvent` method of the parent class to handle any other mouse move events.
    #     Finally, it accepts the event.

    #     Parameters:
    #         event (QMouseEvent): The mouse event object.

    #     Returns:
    #         None
    #     """
    #     if self.initial_pos is not None:
    #         delta = event.pos() - self.initial_pos
    #         self.window().move(
    #             self.window().x() + delta.x(),
    #             self.window().y() + delta.y(),
    #         )
    #     super().mouseMoveEvent(event)
    #     event.accept()

    # def mouseReleaseEvent(self, event) -> None:
    #     """
    #     Handles the mouse release event.

    #     This function is called when the mouse is released. It sets the `initial_pos` variable to `None`.
    #     Then, it calls the `mouseReleaseEvent` method of the parent class to handle any other mouse release events.
    #     Finally, it accepts the event.

    #     Parameters:
    #         event (QMouseEvent): The mouse event object.

    #     Returns:
    #         None
    #     """
    #     self.initial_pos = None
    #     super().mouseReleaseEvent(event)
    #     event.accept()

    def selection_changed(self) -> None:
        """
        Handles the selection changed event.

        This function is called when the selection in the list widget changes. It gets the selected indexes from the list widget.
        Then, it clears the summary model and the aaTab table. It then iterates over the selected indexes and adds the corresponding items to the summary model and the aaTab table.

        Parameters:
            None

        Returns:
            None
        """
        indexes = self.listWidget.selectedIndexes()
        # print(indexes[0].row())
        # self.listWidget.selectionModel().select(
        #     indexes[0], QItemSelectionModel.SelectionFlag.ClearAndSelect
        # )
        # print(self.listModel.index(indexes[0].row(), 0))
        if indexes:
            self.summaryModel._data = []
            self.concentration.extinctions = self.listModel._data[
                indexes[0].row()
            ].extinction
            self.concentration.mass = self.listModel._data[indexes[0].row()].weight
            self.concentration.sequence = self.listModel._data[
                indexes[0].row()
            ].sequence
            self.concentration.name = self.listModel._data[indexes[0].row()].name
            # self.concentration.updateLabels()
            try:
                self.concentration.calcConc()
            except:
                pass
            for index in indexes:
                self.summaryModel._data.append(self.listModel._data[index.row()])
                for aa in self.aacids:
                    count = self.listModel._data[index.row()].aa_counts[aa]
                    self.aaTab.setItem(
                        self.aacids.index(aa), index.row(), QTableWidgetItem(count)
                    )
            self.summaryModel.layoutChanged.emit()

    def clear_selection(self) -> None:
        """
        Handles the clear selection event.

        This function is called when the clear selection button is clicked. It clears the selection in the list widget and the summary model.

        Parameters:
            None

        Returns:
            None
        """
        self.listWidget.clearSelection()
        self.summaryModel._data = []
        self.summaryModel.layoutChanged.emit()
    
    def delete_all(self) -> None:
        preserves.delete_settings()
        self.listModel._data = []
        self.listModel.layoutChanged.emit()


    def add_item(self) -> None:
        """
        Handles the add item event.

        This function is called when the add item button is clicked. It gets the protein name and sequence from the input widget and adds it to the list model.

        Parameters:
            None

        Returns:
            None
        """
        name = self.inputWidget.proteinName.text()
        sequence = self.inputWidget.sequenceEdit.text()
        color = self.inputWidget.colorButton.color()
        if name and sequence:
            self.listModel._data.append(protein(name, sequence, color))
            self.listModel.layoutChanged.emit()

    # def adjust_up(self):
    #     indexes = self.listWidget.selectedIndexes()
    #     if indexes:
    #         if len(indexes) > 1:
    #             self.listWidget.clearSelection()
    #             self.listWidget.setCurrentIndex(indexes[0])
    #         elif indexes[0].row() > 0:
    #             item = self.listWidget.model().index(indexes[0].row(), 0)
    #             self.listModel._data.insert(item.row()-1, self.listModel._data.pop(item.row()))

    def move_up(self) -> None:
        if self.filterList.text() == "":
            index = self.listWidget.currentIndex()
            self.listModel.move_item_up(index.row())
            self.listWidget.clearSelection()
            self.listWidget.setCurrentIndex(
                self.listWidget.model().index(index.row() - 1, 0)
            )
        # self.listWidget.setCurrentIndex(self.listWidget.model().index(index.row()-1, 0), QItemSelectionModel.SelectionFlag.Select)

    def move_down(self) -> None:
        if self.filterList.text() == "":
            index = self.listWidget.currentIndex()
            self.listModel.move_item_down(index.row())
            self.listWidget.clearSelection()
            self.listWidget.setCurrentIndex(
                self.listWidget.model().index(index.row() + 1, 0)
            )

    def delete_item(self) -> None:
        """
        Handles the delete item event.

        This function is called when the delete item button is clicked. It gets the selected indexes from the list widget and deletes them from the list model.

        Parameters:
            None

        Returns:
            None
        """
        indexes = self.listWidget.selectedIndexes()
        if indexes:
            if len(indexes) > 1:
                for item in reversed(sorted(self.listWidget.selectedIndexes())):
                    del self.listModel._data[item.row()]
            else:
                del self.listModel._data[indexes[0].row()]

            self.listModel.layoutChanged.emit()
            self.listWidget.clearSelection()

    # Export data as a fasta file
    def export_data(self) -> None:
        # dialog for saving file
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Export data")
        file_dialog.setNameFilters(["Fasta Files (*.fasta)", "Protein Param Pro (*.P3)"])
        file_dialog.selectNameFilter("Protein Param Pro (*.P3)")
        file_dialog.setDefaultSuffix(".P3")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)

        # file_dialog.exec()
        if file_dialog.exec() == QDialog.Accepted:
            fileName = file_dialog.selectedFiles()[0]
            with open(fileName, "wb") as f:
                data = self.listModel._data
                if fileName.endswith(".P3"):
                    pickle.dump(data, f)
                elif fileName.endswith(".fasta"):
                    for item in data:
                        f.write(f">{item.name}\n{item.sequence}\n")

    # Import data from a fasta file
    def import_data(self) -> None:
        # dialog for loading file
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Import data")
        file_dialog.setNameFilters(["Fasta Files (*.fasta)", "Protein Param Pro (*.P3)"])
        file_dialog.selectNameFilter("Fasta Files (*.fasta)")
        # file_dialog.exec()
        if file_dialog.exec() == QDialog.Accepted:
            fileName = file_dialog.selectedFiles()[0]
            if fileName.endswith(".fasta"):
                with open(fileName, "r", encoding="utf-8") as f:
                    for line in f:
                        if line[0] == ">":
                            name = line[1:].strip()
                            sequence = None
                        else:
                            sequence = line.strip()
                        if name and sequence:                            
                            self.listModel._data.append(protein(name, sequence, color="white"))
            elif fileName.endswith(".P3"):
                with open(fileName, "rb") as f:
                    data = pickle.load(f)
                    for item in data:
                        print(item)
                        self.listModel._data.append(protein(item.name, item.sequence, color=item.color))
            self.listModel.layoutChanged.emit()


def run():
    """
    Runs the application."""
    window = MainWindow()
    window.setWindowTitle(
        f'{PUBLIC_SETTINGS["app_name"]} - Version: {PUBLIC_SETTINGS["version"]}'
    )
    window.resize(500, 500)
    window.show()
    # qdarktheme.setup_theme(['light', 'dark'][preserves.settings.value("pppTheme", type=int)])
    qdarktheme.load_palette()
    return context.app.exec()


if __name__ == "__main__":
    exit_code = run()
    sys.exit(exit_code)
