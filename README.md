# OpenETR

End-verifiable evidence. Consequential state.

![OpenETR logo](./assets/images/openetr-readme.png)

OpenETR is a protocol for deriving consequential state from end-verifiable
evidence concerning durable electronic records.

It gives applications, institutions, and relying parties a shared way to
identify an exact digital artifact, inspect signed evidence concerning it, and
reproduce the state that follows under defined protocol rules. Recognition of
that state, and the legal, commercial, or operational effect it receives,
remain with the relevant community, institution, contract, registry, or law.

## The core model

OpenETR separates four ideas that conventional applications often combine:

- **Digital Artifact**: persistent digital content identified by digest.
- **Digital Controllable Record (DCR)**: one end-verifiable record or a graph
  of related records containing evidence of consequential actions concerning
  an artifact.
- **Consequential State**: state derived by applying defined rules to valid DCR
  evidence.
- **Digital Original**: a Digital Artifact for which consequential state has
  been established through a DCR.

```text
Digital Artifact -> DCR evidence -> Consequential State -> Digital Original

Consequential State -> Recognition -> Effect
```

Applications may store, present, and cache projections of the result. Another
implementation can still validate the signed evidence and reproduce the state
determination without treating the originating application as its sole
authority.

## Where it helps

The same model can support warehouse receipts, bills of lading, product
passports, certificates, credentials, health-record evidence, and other
records whose exact content and consequential history matter.

For a warehouse receipt, sending another copy of the PDF does not transfer the
receipt. The PDF identifies the artifact; valid signed evidence changes the
consequential state. A warehouse, buyer, bank, registry, or court then decides
whether to recognize that state and what effect it has.

OpenETR cooperates with existing systems and institutions. It does not try to
become every domain's registry, legal authority, system of record, or
compliance engine.

## Relationship to Mainstay

OpenETR is an adjacent member of the Mainstay product family, not a service in
the default Mainstay runtime bundle. Mainstay applications can preserve and
present artifacts and evidence; OpenETR defines how consequential state is
derived from qualifying evidence. Local operators and recognition frameworks
remain responsible for policy and effect.

Both projects share a practical goal: information and authority should remain
understandable and usable across applications, operators, and changing
conditions while preserving clear boundaries for trust and governance.

## Initial implementation

The reference implementation uses ordinary Nostr event kinds `1415` and `1416`
for linked, signed records. Prototype kinds `31415` and `31416` are deprecated.
The CLI can issue, query, transfer, encumber, discharge, redeem, and terminate
records.

```bash
poetry install
poetry run openetr profile use warehouse
poetry run openetr issue examples/MLWR001.pdf
poetry run openetr query examples/MLWR001.pdf
```

Transfer control to another configured profile:

```bash
poetry run openetr transfer initiate examples/MLWR001.pdf --transferee exporter
poetry run openetr profile use exporter
poetry run openetr transfer accept examples/MLWR001.pdf
poetry run openetr query examples/MLWR001.pdf
```

## Development and deployment

Check the CLI and build the documentation:

```bash
poetry install
poetry run openetr --help
poetry run mkdocs build --strict
```

Run the standalone web application with Docker:

```bash
cp .env.example .env
# Set OPENETR_APP_SESSION_SECRET to an independently generated value.
docker compose up --build --detach
curl --fail http://127.0.0.1:8000/health
```

See the [installation and deployment guide](docs-site/installation.md) for the
complete standalone lifecycle. The live application is at
[openetr.org](https://openetr.org/).

## Project boundaries

OpenETR proves only what its evidence and rules establish. A valid signature
establishes attribution to a key; it does not by itself establish a person's
identity, legal authority, performance of an outside action, ownership, or
universal recognition.

The project is under active development. Use the current implementation for
evaluation, integration work, and bounded pilots while verifier results,
retrieval coverage, policy adapters, and domain profiles continue to mature.

## Documentation

- [Documentation site](https://trbouma.github.io/openetr/)
- [Specification index](docs/specs/INDEX.md)
- [Consequential State Architecture](docs/specs/CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
- [CLI implementation walkthrough](docs/specs/OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md)
- [Roadmap](docs-site/openetr/roadmap.md)

OpenETR is open-source software released under the MIT License. Contributions
from implementers, domain experts, institutions, standards bodies, and pilot
communities are welcome.
