# Installation And Deployment

Most users should start with the live [OpenETR app](https://openetr.org/). This
page is for developers, operators, and integrators running the app or Python
component themselves.

OpenETR is adjacent to the Mainstay product family but is not part of the
default Mainstay runtime bundle. This guide therefore describes a standalone
OpenETR instance.

## Local Development

From the repository root:

```sh
poetry install
poetry run pip install -r app/requirements.txt
poetry run gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  --reload
```

Then open `http://127.0.0.1:8000/`.

Verify the reusable Python component:

```sh
poetry run python -c "import openetr, openetr.cli; print('openetr import ok')"
poetry run openetr --help
poetry build
```

Build the documentation strictly before committing documentation changes:

```sh
poetry run mkdocs build --strict
```

## Standalone Container Deployment

Use a dedicated checkout or release directory for each instance. Create its
runtime environment and generate a unique session secret:

```sh
cp .env.example .env
openssl rand -hex 32
# Put the generated value in OPENETR_APP_SESSION_SECRET in .env.
docker compose config --quiet
docker compose up --build --detach
```

The supplied Compose configuration binds to `127.0.0.1` by default. Keep that
default when an HTTPS reverse proxy runs on the same host. Select a specific
private LAN or VPN interface only when another machine must reach the service,
and constrain that route with network policy.

The `openetr-data` volume holds the instance's local profile configuration.
Keep it together with the protected `.env`, deployment revision, and operating
policy. Relay-backed evidence remains subject to its own availability and
retention model.

## Verify

```sh
docker compose ps
curl --fail http://127.0.0.1:8000/health
docker compose logs --tail=100 web
```

The health endpoint confirms that the HTTP process responds. It does not prove
relay availability, recognition, signer authority, or the effect of a record.
Verify those concerns through the relevant workflows and policies.

## Update

From the dedicated deployment checkout:

```sh
./refresh-containers.sh
```

The script refuses tracked working-tree changes, performs only a fast-forward
source update, validates Compose, rebuilds and recreates the container, and
waits for the application health check. It does not rotate secrets, change
profiles, or alter recognition policy.

## Back Up, Recover, And Retire

Back up the `openetr-data` volume together with `.env` and the deployment
revision. Stop the container while taking a simple filesystem-level backup so
local configuration is captured consistently. Test recovery without allowing
two active instances to use the same private profile material unintentionally.

`docker compose stop` or `docker compose down` stops the application without
deleting its named volume. Do not use `docker compose down --volumes` for a
routine stop. Retiring keys, records, recognition arrangements, or an
institutional deployment is a separate, explicit process.

## Runtime Configuration

The application recognizes runtime variables including:

| Variable | Purpose |
| --- | --- |
| `OPENETR_APP_SESSION_SECRET` | Required production session-encryption secret |
| `OPENETR_APP_SESSION_SECRET_FILE` | File containing the production session secret |
| `OPENETR_ROOT_NSEC` / `_FILE` | Optional bootstrap root signing key |
| `OPENETR_HOME_RELAYS` / `_FILE` | Optional bootstrap relay set |
| `OPENETR_PUBLIC_BASE_URL` | External HTTPS base URL |
| `OPENETR_MAX_UPLOAD_BYTES` | Maximum accepted upload size |
| `OPENETR_BLOSSOM_SERVER` | Blossom storage endpoint |
| `OPENETR_GIT_COMMIT` | Deployed source revision reported by the app |

Prefer file-based secret inputs when the deployment platform supplies them.

## Suggested Checks

```sh
poetry run python -m py_compile app/main.py
poetry run python -c "from app.main import templates; [templates.env.get_template(t) for t in templates.env.list_templates()]; print('templates parsed')"
poetry run mkdocs build --strict
poetry build
```
