"""
Compound Domain model

"""

class Compound:
    def __init__(
        self, 
        id: int,
        smiles: str,
        molecular_weight: float,
        logp: float,
        h_bond_donor_count: int,
        h_bond_acceptor_count: int
    ) -> None:
        self.id = id
        self.smiles = smiles
        self.molecular_weight = molecular_weight
        self.logp = logp
        self.h_bond_donor_count = h_bond_donor_count
        self.h_bond_acceptor_count = h_bond_acceptor_count
