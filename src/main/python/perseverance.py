from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox
from biocalcs import protein


class Perseverance:
    def __init__(self, parent=None):
        self.settings = QtCore.QSettings("Scientific Studio", "Protein Param Pro")
        if not self.settings.contains("needs_save"):
            self.settings.setValue("needs_save", False)
        # print(self.settings.value("protein0", type=str))
        if not self.settings.contains("protein0"):
            self.settings.setValue("protein0", "Ara h 2")
            self.settings.setValue(
                "sequence0",
                "MAKLTILVALALFLLAAHASARQQWELQGDRRCQSQLERANLRPCEQHLMQKIQRDEDSYERDPYSPSQDPYSPSPYDRRGAGSSQHQERCCNELNEFENNQRCMCEALQQIMENQSDRLQGRQQEQQFKRELRNLPQQCGLRAPQRCDLDVESGG",
            )
            self.settings.setValue("color0", "#62C6F2")
            self.settings.setValue("proteinCount", 1)
        if not self.settings.contains("pppTheme"):
            self.settings.setValue("pppTheme", 0)

    def save_settings(self, main_self):
        print("Saved!")
        count = len(main_self.listModel._data)
        self.settings.setValue("proteinCount", count)
        print(count)
        for i in range(count):
            self.settings.setValue(f"protein{i}", main_self.listModel._data[i].name)
            self.settings.setValue(
                f"sequence{i}", main_self.listModel._data[i].sequence
            )
            if main_self.listModel._data[i].color == "":
                self.settings.setValue(f"color{i}", "#FFFFFF")
            else:
                self.settings.setValue(f"color{i}", main_self.listModel._data[i].color)
        self.settings.setValue("pppTheme", main_self.pppTheme)
        print(self.settings.value("protein0", type=str))

    def delete_settings(self):
        dlg = QMessageBox()
        dlg.setWindowTitle("Delete Settings?")
        dlg.setText("Are you sure you want to delete all settings?")
        dlg.setIcon(QMessageBox.Icon.Question)
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        dlg.setDefaultButton(QMessageBox.StandardButton.No)
        ret = dlg.exec()
        if ret == QMessageBox.StandardButton.Yes:
            for i in range(self.settings.value("proteinCount", type=int)):
                self.settings.remove(f"protein{i}")
                self.settings.remove(f"sequence{i}")
                self.settings.remove(f"color{i}")
            self.settings.clear()
            self.settings.setValue("proteinCount", 0)
            self.settings.setValue("needs_save", False)
            print("Deleted!")


    def load_settings(self, main_self):
        # print("Loaded!")
        count = self.settings.value("proteinCount", type=int)
        # print(count)
        for i in range(count):
            name = self.settings.value(f"protein{i}", type=str)
            sequence = self.settings.value(f"sequence{i}", type=str)
            color = self.settings.value(f"color{i}", type=str)
            if color == "":
                color = "white"
            main_self.listModel._data.append(protein(name, sequence, color))
        main_self.pppTheme = self.settings.value("pppTheme", type=int)

    def len(self):
        return len(self.settings.value("sequence", type=str))
