from PySide6 import QtCore
from biocalcs import protein


class Perseverance:
    def __init__(self, parent=None):
        self.settings = QtCore.QSettings("Scientific Studio", 'Protein Param Pro')
        # print(self.settings.value("protein0", type=str))
        if not self.settings.contains("protein0"):
            self.settings.setValue("protein0", "Ara h 2")
            self.settings.setValue(
                "sequence0",
                "MAKLTILVALALFLLAAHASARQQWELQGDRRCQSQLERANLRPCEQHLMQKIQRDEDSYERDPYSPSQDPYSPSPYDRRGAGSSQHQERCCNELNEFENNQRCMCEALQQIMENQSDRLQGRQQEQQFKRELRNLPQQCGLRAPQRCDLDVESGG",
            )
            self.settings.setValue("proteinCount", 1)
        if not self.settings.contains("pppTheme"):
            self.settings.setValue("pppTheme", 0)

    def save_settings(self, main_self):
        print("Saved!")
        count = len(main_self.mainWidget.listWidget.listModel._data)
        self.settings.setValue("proteinCount", count)
        print(count)
        for i in range(count):
            self.settings.setValue(f"protein{i}", main_self.mainWidget.listModel._data[i].name)
            self.settings.setValue(
                f"sequence{i}", main_self.mainWidget.listModel._data[i].sequence
            )
        self.settings.setValue("pppTheme", main_self.pppTheme)
        print(self.settings.value("protein0", type=str))

    def delete_settings(self):
        print("Deleted!")
        self.settings.clear()

    def load_settings(self, main_self):
        # print("Loaded!")
        count = self.settings.value("proteinCount", type=int)
        # print(count)
        for i in range(count):
            name = self.settings.value(f"protein{i}", type=str)
            sequence = self.settings.value(f"sequence{i}", type=str)
            main_self.listWidget.listModel._data.append(protein(name, sequence))
        main_self.pppTheme = self.settings.value("pppTheme", type=int)

    def len(self):
        return len(self.settings.value("sequence", type=str))
