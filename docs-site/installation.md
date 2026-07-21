# Installation And Local Development

Most users should start with the live OpenETR app:

```text
https://openetr.org/
```

Warehouse receipt users can go directly to:

```text
https://openetr.org/warehouse-receipts
```

Product Passport users can go directly to:

```text
https://openetr.org/digital-product-passports
```

This page is for developers, operators, and integrators who want to run the app locally, build the documentation site, or deploy the Docker container.

## Run The Webapp Locally

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

## Local Documentation Site

Install the documentation dependency through Poetry:

```sh
poetry add --group dev mkdocs-material
```

Serve the docs locally:

```sh
poetry run mkdocs serve
```

Build the docs strictly before committing documentation changes:

```sh
poetry run mkdocs build --strict
```

## Python Component

The installable Python component is `openetr`.

Verify it installs and imports:

```sh
poetry install
poetry run python -c "import openetr, openetr.cli; print('openetr import ok')"
poetry run openetr --help
```

Build package artifacts:

```sh
poetry build
```

## Docker Deployment

The webapp Docker image is built from the repository root:

```sh
docker build -f app/Dockerfile -t openetr-web .
```

The Dockerfile installs the reusable `openetr` component and then installs the app-only FastAPI dependencies from `app/requirements.txt`.

For relay-backed operation, provide runtime environment variables such as:

```text
OPENETR_APP_SESSION_SECRET
OPENETR_ROOT_NSEC
OPENETR_HOME_RELAYS
OPENETR_SITE_URL
OPENETR_GIT_COMMIT
```

## Suggested Local Checks

For docs changes:

```sh
poetry run mkdocs build --strict
```

For app changes:

```sh
poetry run python -m py_compile app/main.py
poetry run python -c "from app.main import templates; [templates.env.get_template(t) for t in templates.env.list_templates()]; print('templates parsed with app env')"
```

For package checks:

```sh
poetry install
poetry run openetr --help
poetry build
```
