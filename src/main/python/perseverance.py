from PySide2 import QtCore
from biocalcs import protein

class Perseverance():
    def __init__(self, parent=None):
        self.settings = QtCore.QSettings()
        print(self.settings.value("protein0", type=str))
        if not self.settings.contains("protein0"):
            self.settings.setValue("protein0", "Ara h 3")
            self.settings.setValue("sequence0", "ISFRQQPEENACQFQRLNAQRPDNRIESEGGYIETWNPNNQEFECAGVALSRLVLRRNALRRPFYSNAPQEIFIQQGRGYFGLIFPGCPSTYEEPAQQGRRYQSQRPPRRLQEEDQSQQQQDSHQKVHRFNEGDLIAVPTGVAFWLYNDHDTDVVAVSLTDTNNNDNQLDQFPRRFNLAGNHEQEFLRYQQQSRQSRRRSLPYSPYSPQSQPRQEEREFSPRGQHSRRERAGQEEEHEGGNIFSGFTPEFLAQAFQVDDRQIVQNLRGENESEEQGAIVTVRGGLRILSPDRKRGADEEEEYDEDEYEYDEEDRRRGRGSRGSGNGIEETICTATVKKNIGRNRSPDIYNPQAGSLKTANELNLLILRWLGLSAEYGNLYRNALFVPHYNTNAHSIIYALRGRAHVQVVDSNGNRVYDEELQEGHVLVVPQNFAVAGKSQSDNFEYVAFKTDSRPSIANLAGENSVIDNLPEEVVANSYGLPREQARQLKNNNPFKFFVPPSQQSPRAVA")

    def save_settings(self, main_self):
        print("Saved!")
        count = len(main_self.listModel._data)
        self.settings.setValue("proteinCount", count)
        print(count)
        for i in range(count):
            self.settings.setValue(f"protein{i}", main_self.listModel._data[i].name)
            self.settings.setValue(f"sequence{i}", main_self.listModel._data[i].sequence)
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
            main_self.listModel._data.append(protein(name, sequence))
    
    def len(self):
        return len(self.settings.value("sequence", type=str))