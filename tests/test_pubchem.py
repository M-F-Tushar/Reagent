"""Tests for Week 1 PubChem acquisition."""

from types import SimpleNamespace

import pubchempy as pcp
import pytest

from reagent.domain.compound import Compound
from reagent.ingestion.pubchem import (
    DEFAULT_ASSAY_ID,
    fetch_compounds_from_assay,
)


def test_acquisition_builds_compound_objects(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get_json(
        assay_id: int,
        *,
        namespace: str,
        domain: str,
        operation: str,
        cids_type: str,
    ) -> dict[str, dict[str, list[int]]]:
        assert assay_id == DEFAULT_ASSAY_ID
        assert namespace == "aid"
        assert domain == "assay"
        assert operation == "cids"
        assert cids_type == "active"
        return {"IdentifierList": {"CID": [1, 2]}}

    monkeypatch.setattr(pcp, "get_json", fake_get_json)
    records = [
        SimpleNamespace(
            cid=compound_id,
            smiles="CCO",
            molecular_weight=46.07,
            xlogp=-0.3,
            h_bond_donor_count=1,
            h_bond_acceptor_count=1,
        )
        for compound_id in (1, 2)
    ]
    monkeypatch.setattr(pcp, "get_compounds", lambda *args, **kwargs: records)

    compounds = fetch_compounds_from_assay(limit=2)

    assert len(compounds) == 2
    assert all(isinstance(compound, Compound) for compound in compounds)


def test_acquisition_rejects_non_positive_limit() -> None:
    with pytest.raises(ValueError, match="limit must be at least 1"):
        fetch_compounds_from_assay(limit=0)


@pytest.mark.live
def test_live_acquisition_returns_at_least_50_compounds() -> None:
    try:
        compounds = fetch_compounds_from_assay(
            assay_id=DEFAULT_ASSAY_ID,
            limit=50,
        )
    except (OSError, RuntimeError, pcp.PubChemPyError) as error:
        pytest.skip(f"PubChem is unavailable: {error}")

    assert len(compounds) >= 50