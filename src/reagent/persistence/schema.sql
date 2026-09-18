CREATE TABLE IF NOT EXISTS targets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    organism TEXT NOT NULL,
    accession TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS assays (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    target_id INTEGER,
    FOREIGN KEY (target_id) REFERENCES targets (id)
);

CREATE TABLE IF NOT EXISTS compounds (
    id INTEGER PRIMARY KEY,
    smiles TEXT NOT NULL,
    molecular_weight REAL NOT NULL,
    logp REAL NOT NULL,
    h_bond_donor_count INTEGER NOT NULL,
    h_bond_acceptor_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS assay_compounds (
    assay_id INTEGER NOT NULL,
    compound_id INTEGER NOT NULL,
    PRIMARY KEY (assay_id, compound_id),
    FOREIGN KEY (assay_id) REFERENCES assays (id),
    FOREIGN KEY (compound_id) REFERENCES compounds (id)
);