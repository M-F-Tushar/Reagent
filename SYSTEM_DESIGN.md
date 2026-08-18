# System Design

## Product vision

Reagent is both a molecular drug-discovery platform and a guided, 16-week course of study. The finished product turns public chemical and biological data into an explorable workflow:

1. A user searches for a disease-related protein or biological target.
2. Reagent retrieves real compounds and bioactivity measurements from sources such as ChEMBL and PubChem.
3. The platform normalizes and stores the records, preserving both structured entities and source documents.
4. Drug-likeness rules remove unsuitable candidates and explain each decision.
5. Hand-implemented algorithms rank, search, and compare molecular fingerprints to find similar compounds.
6. A knowledge graph connects drugs, targets, diseases, and evidence so the user can investigate repurposing opportunities.
7. An API and demonstration interface expose the complete workflow.

Reagent supports learning and exploration; it does not make clinical claims or replace laboratory validation, medical judgment, or regulatory review.

## Major technical decisions

### PostgreSQL and MongoDB

PostgreSQL is the system of record for well-structured, related data such as targets, compounds, assays, activities, and provenance. Its constraints, transactions, joins, indexes, and query planner make DBMS concepts visible and protect data integrity. MongoDB complements it by retaining heterogeneous source documents and flexible metadata whose shape can vary between providers. Using both databases teaches when relational normalization is valuable, when document storage is appropriate, and how a polyglot system avoids forcing every kind of data into one model.

### FastAPI

FastAPI provides a typed HTTP boundary around ingestion, search, filtering, similarity, and graph capabilities. Its integration with Pydantic makes request and response contracts explicit, generates interactive API documentation, and keeps validation near the service boundary. It is lightweight enough for teaching while following production-oriented API practices.

### Docker and Docker Compose

Docker gives the student, CI, and demonstrations the same repeatable runtime environment. Docker Compose describes how the API, PostgreSQL, MongoDB, and later UI services run together without requiring hand-configured local installations. Services are introduced only when their roadmap week needs them, keeping the learning sequence incremental.

