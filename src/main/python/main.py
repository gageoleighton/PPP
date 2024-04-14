'Application Corrupt run xattr -cr /path/to/application.app'

from fbs_runtime.application_context.PySide2 import ApplicationContext
from fbs_runtime import PUBLIC_SETTINGS

import sys

from PySide2.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
    QListView, QTableWidget, QTabWidget, QTableWidgetItem, QFileDialog, QAction,
    QSizePolicy
)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QEvent

import qdarktheme

from customtitlebar import CustomTitleBar

from inputwidget import inputWidget
from summarytable import summaryTable, summaryModel
from concentration import Concentration

from mainlistview import MainList, ListModel
from biocalcs import *

from Bio import SeqIO

from perseverance import Perseverance

from customwidgets import *

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.preserves = Perseverance()
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
        import_action.triggered.connect(self.inport_data)

        export_action = QAction("&Export", self)
        export_action.setShortcut("Ctrl+E")
        # export_action.setDisabled(True)
        export_action.triggered.connect(self.export_data)
        # export_action.triggered.connect(lambda: self.preserves.export_settings(self))

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(lambda: self.preserves.save_settings(self))

        delete_save_action = QAction("&Delete Save", self)
        delete_save_action.setShortcut("Ctrl+D")
        delete_save_action.triggered.connect(self.preserves.delete_settings)

        exit_action = QAction(" E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(QApplication.closeAllWindows)

        file_menu.addActions([import_action, export_action, save_action, delete_save_action, exit_action])

        help_menu = menu.addMenu("&Help")

        about_action = QAction("&About...", self)
        about_action.triggered.connect(aboutDialog)

        help_menu.addActions([about_action])

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

        self.bottomBar = QWidget()
        self.bottomBarLayout = QHBoxLayout()
        self.bottomBar.setLayout(self.bottomBarLayout)

        self.windowScaleButton = QPushButton("#")
        self.windowScaleButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.windowScaleButton.setCursor(Qt.SizeFDiagCursor)
        self.bottomBarLayout.addWidget(self.windowScaleButton)
        self.bottomBarLayout.addStretch()
        self.bottomBarLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.bottomBar, alignment=Qt.AlignRight)

        self.leftLayout = QVBoxLayout()

        self.addRemoveLayout = QHBoxLayout()

        self.addButton = QPushButton("Add")
        self.addRemoveLayout.addWidget(self.addButton)
        self.addButton.clicked.connect(self.add_item)

        self.removeButton = QPushButton("Delete")
        self.addRemoveLayout.addWidget(self.removeButton)
        self.removeButton.clicked.connect(self.delete_item)

        self.leftLayout.addLayout(self.addRemoveLayout)
        self.layout.addLayout(self.leftLayout)

        self.listWidget = MainList()
        self.leftLayout.addWidget(self.listWidget)
        # self.listWidget.selectionModel().selectionChanged.connect(self.selection_changed)
        self.listWidget.setSelectionMode(QListView.SelectionMode.MultiSelection)
        # self.listView.clicked.connect(self.listView.clearSelection)

        self.listModel = ListModel()
        self.listWidget.setModel(self.listModel)
        self.listWidget.doubleClicked.connect(self.clear_selection)
        self.listWidget.selectionModel().selectionChanged.connect(self.selection_changed)

        self.adjustListLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.adjustListLayout)
        self.adjustUp = QPushButton("Up")
        self.adjustDown = QPushButton("Down")
        self.adjustListLayout.addWidget(self.adjustUp)
        self.adjustListLayout.addWidget(self.adjustDown)
        self.adjustUp.clicked.connect(self.move_up)
        self.adjustDown.clicked.connect(self.move_down)

# Settings -----------------------------------------------------------------------------
        
        self.tabWidget = QTabWidget()
        self.layout.addWidget(self.tabWidget)

        self.inputWidget = inputWidget(self.preserves)
        self.tabWidget.addTab(self.inputWidget, "Input")

        self.summaryTable = summaryTable(self.preserves)
        self.tabWidget.addTab(self.summaryTable, "Summary")
        self.summaryTable.setSelectionMode(QListView.SelectionMode.MultiSelection)
        self.summaryTable.setSelectionBehavior(QListView.SelectionBehavior.SelectRows)

        self.summaryModel = summaryModel(self.preserves)
        self.summaryTable.setModel(self.summaryModel)

        self.aaTab = QTableWidget()
        self.tabWidget.addTab(self.aaTab, "Amino acids")
        self.aacids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
        self.aaTab.setVerticalHeaderLabels(self.aacids)

        self.concentration = Concentration()
        self.tabWidget.addTab(self.concentration, "Concentration")

        # self.proteinModel.layoutChanged.emit()

        self.setCentralWidget(self.mainWidget)

        self.preserves.load_settings(self)


    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()

    def window_state_changed(self, state):
        self.normal_button.setVisible(state == Qt.WindowState.WindowMaximized)
        self.max_button.setVisible(state != Qt.WindowState.WindowMaximized)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.pos()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.pos() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

    def selection_changed(self):
        indexes = self.listWidget.selectedIndexes()
        # print(indexes)
        if indexes:
            self.summaryModel._data = []
            self.concentration.extinctions = self.listModel._data[indexes[0].row()].extinction
            self.concentration.mass = self.listModel._data[indexes[0].row()].weight
            # self.concentration.updateLabels()
            try:
                self.concentration.calcConc()
            except:
                pass
            for index in indexes:
                self.summaryModel._data.append(self.listModel._data[index.row()])
                for aa in self.aacids:
                    count = self.listModel._data[index.row()].aa_counts[aa]
                    self.aaTab.setItem(self.aacids.index(aa), index.row(), QTableWidgetItem(count))
            self.summaryModel.layoutChanged.emit()
    
    def clear_selection(self):
        self.listWidget.clearSelection()
        self.summaryModel._data = []
        self.summaryModel.layoutChanged.emit()
    
    def add_item(self):
        name = self.inputWidget.proteinName.text()
        sequence = self.inputWidget.sequenceEdit.text()
        if name and sequence:
            self.listModel._data.append(protein(name, sequence))
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
    
    def move_up(self):
        index = self.listWidget.currentIndex()
        self.listModel.move_item_up(index.row())
        self.listWidget.clearSelection()
        self.listWidget.setCurrentIndex(self.listWidget.model().index(index.row()-1, 0))
        # self.listWidget.setCurrentIndex(self.listWidget.model().index(index.row()-1, 0), QItemSelectionModel.SelectionFlag.Select)

    def move_down(self):
        index = self.listWidget.currentIndex()
        self.listModel.move_item_down(index.row())
        self.listWidget.clearSelection()
        self.listWidget.setCurrentIndex(self.listWidget.model().index(index.row()+1, 0))

    def delete_item(self):
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
    def export_data(self):
        # dialog for saving file        
        fileName, _ = QFileDialog.getSaveFileName(self, "Export data", "","Fasta Files (*.fasta)")
        if fileName:
            with open(fileName, 'w') as f:
                data = self.listModel._data
                for item in data:
                    f.write(f">{item.name}\n{item.sequence}\n")
    
    # Import data from a fasta file
    def import_data(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Import data", "", "Fasta Files (*.fasta)")
        if fileName:
            with open(fileName, 'r') as f:
                for line in f:
                    if line[0] == ">":
                        name = line[1:].strip()
                        sequence = ""
                    else:
                        sequence += line.strip()
                self.listModel._data.append(protein(name, sequence))
                self.listModel.layoutChanged.emit()
    
    def inport_data(self):
        # dialog for loading file
        fileName, _ = QFileDialog.getOpenFileName(self, "Import data", "", "Fasta Files (*.fasta)")
        if fileName:
            with open(fileName, 'r') as f:
                for record in SeqIO.parse(f, "fasta"):
                    # print(record.description, record.seq)
                    name = record.description
                    sequence = str(record.seq)
                    self.listModel._data.append(protein(name, sequence))
                self.listModel.layoutChanged.emit()

class AppContext(ApplicationContext):
    def __init__(self):
        super().__init__()

    def run(self):
        window = MainWindow()
        window.setWindowTitle(f'{PUBLIC_SETTINGS["app_name"]} - Version: {PUBLIC_SETTINGS["version"]}')
        self.app.setWindowIcon(QIcon(self.get_resource("close.svg")))
        window.resize(500, 500)
        window.show()
        qdarktheme.setup_theme()
        return self.app.exec_()  

if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)