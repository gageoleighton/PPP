from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSplitter, QSizePolicy, QTabWidget, QListView
from PySide6.QtCore import Qt
from base import preserves
from filterwidget import FilterWidget
from mainlistview import MainList, ListModel
from inputwidget import inputWidget
from summarytable import summaryTable, summaryModel
from concentration import Concentration

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.layout = QHBoxLayout()
        # self.layout.setContentsMargins(11, 11, 0, 0)
        # self.mainLayout.addWidget(self.title_bar)
        self.mainLayout.addLayout(self.layout)

        self.leftLayout = QVBoxLayout()

        self.addRemoveLayout = QHBoxLayout()

        self.addButton = QPushButton("Add")
        self.addRemoveLayout.addWidget(self.addButton)
        # self.addButton.clicked.connect(self.add_item)

        self.removeButton = QPushButton("Delete")
        self.addRemoveLayout.addWidget(self.removeButton)
        # self.removeButton.clicked.connect(self.delete_item)

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

        # self.listModel = ListModel()
        # self.listWidget.setModel(self.listModel)
        self.addButton.clicked.connect(lambda: self.listWidget.add_item(self.inputWidget.proteinName.text(), self.inputWidget.sequenceEdit.text()))
        self.removeButton.clicked.connect(self.listWidget.delete_item)
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

        # self.aaTab = aaTab()
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
        # self.aaTab.setVerticalHeaderLabels(self.aacids)

        self.concentration = Concentration()
        self.tabWidget.addTab(self.concentration, "Concentration")

        # self.proteinModel.layoutChanged.emit()

        # self.setCentralWidget(self.mainWidget)

        preserves.load_settings(self)
    
    def clear_selection(self) -> None:
        self.listWidget.clearSelection()
        self.summaryModel._data = []
        self.summaryModel.layoutChanged.emit()
    
    def selection_changed(self) -> None:
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
                    # self.aaTab.setItem(
                    #     self.aacids.index(aa), index.row(), QTableWidgetItem(count)
                    # )
            self.summaryModel.layoutChanged.emit()
    
    def move_up(self) -> None:
        index = self.listWidget.currentIndex()
        self.listModel.move_item_up(index.row())
        self.listWidget.clearSelection()
        self.listWidget.setCurrentIndex(
            self.listWidget.model().index(index.row() - 1, 0)
        )
        # self.listWidget.setCurrentIndex(self.listWidget.model().index(index.row()-1, 0), QItemSelectionModel.SelectionFlag.Select)

    def move_down(self) -> None:
        index = self.listWidget.currentIndex()
        self.listModel.move_item_down(index.row())
        self.listWidget.clearSelection()
        self.listWidget.setCurrentIndex(
            self.listWidget.model().index(index.row() + 1, 0)
        )