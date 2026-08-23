from reagent.ingestion.pubchem import (
    DEFAULT_ASSAY_ID,
    fetch_compounds_from_assay,
)


def main() -> None:
    """Demonstrate instances by printing properties stored on each ``Compound``."""
    compounds = fetch_compounds_from_assay()
    print(f"PubChem BioAssay AID {DEFAULT_ASSAY_ID}: {len(compounds)} compounds")
    for compound in compounds:
        print(
            f"id={compound.id}, smiles={compound.smiles}, "
            f"molecular_weight={compound.molecular_weight}, logp={compound.logp}, "
            f"h_bond_donor_count={compound.h_bond_donor_count}, "
            f"h_bond_acceptor_count={compound.h_bond_acceptor_count}"
        )


if __name__ == "__main__":
    main()