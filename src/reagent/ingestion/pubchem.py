# Retrive compounds from a PubChem BioAssay and Converts each PubChem record into a Reagent Compound object.

from typing import Any # Can be any type, We don't know the third party object

import pubchempy as pcp

from reagent.domain.compound import Compound

DEFAULT_ASSAY_ID = 485341
DEFAULT_COMPOUND_LIMIT = 100
_PUBCHEM_BATCH_SIZE = 100


def _active_compound_ids(assay_id: int) -> list[int]: 
    """
    Retured integers are PubChem compound IDs, also called CIDs.
    """
    response = pcp.get_json(
        assay_id,
        namespace="aid", # aid means BioAssay identifier.
        domain = "assay",
        operation = "cids",
        cids_type = "active"
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
    