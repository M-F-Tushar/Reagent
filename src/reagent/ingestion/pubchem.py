"""Acquire Week 1 compound records from a PubChem BioAssay."""

from typing import Any

import pubchempy as pcp

from reagent.domain.compound import Compound

DEFAULT_ASSAY_ID = 485341
DEFAULT_COMPOUND_LIMIT = 100
_PUBCHEM_BATCH_SIZE = 100


def _active_compound_ids(assay_id: int) -> list[int]:
    """Return active compound IDs for conversion into typed OOP instances."""
    response = pcp.get_json(
        assay_id,
        namespace="aid",
        domain="assay",
        operation="cids",
        cids_type="active",
    )
    if not response:
        raise RuntimeError(f"PubChem BioAssay {assay_id} returned no response")

    try:
        compound_ids = response["IdentifierList"]["CID"]
    except (KeyError, TypeError) as error:
        raise RuntimeError(
            f"PubChem BioAssay {assay_id} returned no active compound IDs"
        ) from error

    return [int(compound_id) for compound_id in compound_ids]


def _to_compound(pubchem_compound: Any) -> Compound | None:
    """Demonstrate OOP modeling by converting one provider record to an instance."""
    cid = pubchem_compound.cid
    smiles = pubchem_compound.smiles
    molecular_weight = pubchem_compound.molecular_weight
    logp = pubchem_compound.xlogp
    donor_count = pubchem_compound.h_bond_donor_count
    acceptor_count = pubchem_compound.h_bond_acceptor_count

    if any(
        value is None
        for value in (
            cid,
            smiles,
            molecular_weight,
            logp,
            donor_count,
            acceptor_count
        )
    ):
        return None

    return Compound(
        id=int(cid),
        smiles=str(smiles),
        molecular_weight=float(molecular_weight),
        logp=float(logp),
        h_bond_donor_count=int(donor_count),
        h_bond_acceptor_count=int(acceptor_count),
    )


def fetch_compounds_from_assay(
    assay_id: int = DEFAULT_ASSAY_ID,
    limit: int = DEFAULT_COMPOUND_LIMIT,
) -> list[Compound]:
    """Demonstrate OOP by returning external records as ``Compound`` instances.

    PubChemPy retrieves both the assay's active compound IDs and each compound's
    molecular properties. Records missing a required Week 1 property are skipped.
    """
    if limit < 1:
        raise ValueError("limit must be at least 1")

    compound_ids = _active_compound_ids(assay_id)
    compounds: list[Compound] = []

    for start in range(0, len(compound_ids), _PUBCHEM_BATCH_SIZE):
        batch_ids = compound_ids[start : start + _PUBCHEM_BATCH_SIZE]
        records = pcp.get_compounds(batch_ids, namespace="cid")
        for record in records:
            compound = _to_compound(record)
            if compound is not None:
                compounds.append(compound)
                if len(compounds) == limit:
                    return compounds

    return compounds