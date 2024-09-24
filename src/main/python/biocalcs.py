from Bio.SeqUtils.IsoelectricPoint import IsoelectricPoint as IP
from Bio.SeqUtils.ProtParam import ProteinAnalysis

def rolling_pi(sequence, bin):
    data = []
    for i in range(len(sequence) - bin):
        subsequence = sequence[i:i+bin]
        data.append(IP(subsequence).pi())
    return data
    

# def analyze_protein(sequence):
#     weight = calc_mw(sequence)

class protein():
    def __init__(self, name, sequence, color):
        self.name = name or "Undefined"
        self.sequence = sequence
        self.color = color or "white"
        if sequence:
            self.analysis = ProteinAnalysis(sequence)
            self.weight = self.analysis.molecular_weight()
            self.pI = self.analysis.isoelectric_point()
            self.extinction = self.analysis.molar_extinction_coefficient()
            self.aromaticity = self.analysis.aromaticity()
            # self.flexibility = self.analysis.flexibility()
            self.aa_counts = self.analysis.count_amino_acids()
            # print(self.aa_counts.keys())
            self.data = {'Name': self.name, 'Sequence': self.sequence, 'pI': self.pI, 'Extinction Reduced': self.extinction[0], 'Extinction Disulfide': self.extinction[1], 'Weight (KDa)': self.weight/1000, 'Aromaticity': self.aromaticity, 'AA Counts': self.aa_counts, 'color': self.color}

    def __repr__(self):
        return str(self.data)