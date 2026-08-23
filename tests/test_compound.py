from reagent.domain.compound import Compound

def test_compound_construction() -> None:
    compound = Compound(
        id = 2244,
        smiles="CCO",
        molecular_weight=46.07,
        logp=-0.3,
        h_bond_donor_count=1,
        h_bond_acceptor_count=1
    )

    assert compound.id == 2244
    assert compound.smiles == "CCO"
    assert compound.molecular_weight == 46.07
    assert compound.logp == -0.3
    assert compound.h_bond_donor_count == 1
    assert compound.h_bond_acceptor_count == 1

def test_compound_str() -> None:
    compound = Compound(
        id = 2244,
        smiles="CCO",
        molecular_weight=46.07,
        logp=-0.3,
        h_bond_donor_count=1,
        h_bond_acceptor_count=1
    )

    assert isinstance(compound.id, int)
    assert isinstance(compound.smiles, str)
    assert isinstance(compound.molecular_weight, float)
    assert isinstance(compound.logp, float)
    assert isinstance(compound.h_bond_donor_count, int)
    assert isinstance(compound.h_bond_acceptor_count, int)
