# Getting Started

## Run The Webapp

From the repository root:

```sh
cd /Users/trbouma/projects/etrix
poetry install
pip install -r app/requirements.txt
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

The landing page is the **MLWR Control Desk**.

## Use The Control Desk

The Control Desk supports two broad modes.

| Mode | What You Can Do |
| --- | --- |
| Read-only | Query a receipt document by uploading the file and recomputing its digest. |
| Signed in | Select a profile, issue receipt origin events, and publish control records. |

When signed in, the landing page shows:

- the current root identity;
- the selected acting profile;
- a profile selector;
- a Backup Key action for recovery material.

## Key Safety

The **Control Desk Key** is the root/admin key for the workspace.

It can organize profiles and recover relay-backed configuration. It should be safeguarded and kept distinct from day-to-day operational profile keys.

The Backup Key dialog copies recovery material only after an explicit user action.

## CLI Equivalents

The same workflow can be exercised from the CLI:

```sh
openetr profile use warehouse
openetr issue-etr examples/mlwr-20260713.pdf
openetr query-etr examples/mlwr-20260713.pdf
```

For machine-readable automation:

```sh
openetr issue-etr examples/mlwr-20260713.pdf --json
openetr query-etr examples/mlwr-20260713.pdf --json
```

See also:

- [OpenETR CLI JSON Model](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_CLI_JSON_MODEL.md)
- [OpenETR CLI Implementation Walkthrough](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md)

