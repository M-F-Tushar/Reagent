"""Load the 100 compounds into SQLite."""

import sqlite3
from collections.abc import Iterable
from pathlib import Path

from reagent.domain.compound import Compound
from reagent.ingestion.pubchem import (
    DEFAULT_ASSAY_ID,
    DEFAULT_COMPOUND_LIMIT,
    fetch_compounds_from_assay,
)
from reagent.persistence import (
    DEFAULT_DATABASE_PATH,
    connect_database,
    create_schema,
)

ASSAY_NAME = "qHTS Inhibitors of AmpC Beta-Lactamase (assay without detergent)"


def load_compounds(
    connection: sqlite3.Connection,
    compounds: Iterable[Compound],
    assay_id: int = DEFAULT_ASSAY_ID,
) -> int:
    """Store compounds and return how many input objects were processed."""
    connection.execute(
        """
        INSERT INTO assays (id, name, description, target_id)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """,
        (assay_id, ASSAY_NAME, "Active compounds acquired from PubChem.", None),
    )

    loaded_count = 0
    for compound in compounds:
        connection.execute(
            """
            INSERT INTO compounds (
                id,
                smiles,
                molecular_weight,
                logp,
                h_bond_donor_count,
                h_bond_acceptor_count
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                smiles = excluded.smiles,
                molecular_weight = excluded.molecular_weight,
                logp = excluded.logp,
                h_bond_donor_count = excluded.h_bond_donor_count,
                h_bond_acceptor_count = excluded.h_bond_acceptor_count
            """,
            (
                compound.id,
                compound.smiles,
                compound.molecular_weight,
                compound.logp,
                compound.h_bond_donor_count,
                compound.h_bond_acceptor_count,
            ),
        )
        connection.execute(
            """
            INSERT INTO assay_compounds (assay_id, compound_id)
            VALUES (?, ?)
            ON CONFLICT(assay_id, compound_id) DO NOTHING
            """,
            (assay_id, compound.id),
        )
        loaded_count += 1

    connection.commit()
    return loaded_count


def load_week_1_compounds(
    database_path: str | Path = DEFAULT_DATABASE_PATH,
) -> int:
    """Fetch and persist exactly the 100 compounds selected in Week 1."""
    compounds = fetch_compounds_from_assay(limit=DEFAULT_COMPOUND_LIMIT)
    if len(compounds) != DEFAULT_COMPOUND_LIMIT:
        raise RuntimeError(
            f"expected {DEFAULT_COMPOUND_LIMIT} complete compounds, "
            f"received {len(compounds)}"
        )

    with connect_database(database_path) as connection:
        create_schema(connection)
        return load_compounds(connection, compounds)


def main() -> None:
    """Build the Week 2 database from the Week 1 acquisition."""
    loaded_count = load_week_1_compounds()
    print(f"Loaded {loaded_count} compounds into {DEFAULT_DATABASE_PATH}")


if __name__ == "__main__":
    main()