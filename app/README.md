# Demo App

This directory contains a demonstration FastAPI app that is intentionally kept separate from the installable `openetr` component.

## Separation Rationale

The root Poetry package defines `openetr` as the installable component. Files and dependencies under `app/` do not become part of that component unless the root packaging configuration is explicitly changed.

This keeps:

- the reusable `openetr` package clean
- FastAPI and app-only dependencies out of the core component
- the demo web app free to evolve independently

## Install

Use Python 3.11-3.13 and Poetry 2.2 or newer. OpenETR uses Stroma rather than
Monstr for Nostr operations. Existing keys and relay-backed profiles remain
compatible. When upgrading a Python 3.10 virtualenv, select a supported interpreter
with `poetry env use python3.12` before installing both component and app dependencies.
Docker deployments need an image rebuild, not only a restart.

Install the component from the repo root if you want the app to import package code later:

```sh
poetry install
```

Install app-only dependencies separately:

```sh
pip install -r app/requirements.txt
```

This installs the web-only dependencies used by the demo app, including FastAPI, Jinja templates, multipart upload support, Gunicorn, and session-cookie support.

## Run

From the repo root:

```sh
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --reload
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## Current Demo

The current demo app renders an OpenETR `query-etr` style result page from an uploaded file digest.

In app terminology, the uploaded receipt or document is a **Digital Artifact** identified by its digest. The first signed record is its **Anchor Record**. The Anchor and later signed control records form a candidate **Digital Controllable Record (DCR)**. OpenETR validates that record graph under a stated verifier policy and derives **Consequential State**; external law, registries, contracts, and institutional policy determine recognition and legal effect.

Uploads are limited to 10 MiB by default. Set `OPENETR_MAX_UPLOAD_BYTES` to override the limit for a deployment.

When the uploaded file is a PDF or supported image, the result page also shows an inline preview. Preview files are temporary, tokenized, served with `Cache-Control: no-store`, and cleaned up after one hour. PDFs render through the bundled PDF.js assets under `app/assets/js`.

Create-control-record upload forms can optionally store the raw uploaded file using
Stroma's `BlossomPool`. Storage remains opt-in: selecting it sends the artifact to
all configured servers, authorized by short-lived events signed by the Acting
Profile. Only servers that return digest-matching bytes are advertised in repeated
`blossom` tags on the new anchor, before it is signed. No existing anchor is
rewritten to change locations.

The default remains `https://blossom.getsafebox.app`. The legacy
`OPENETR_BLOSSOM_SERVER` setting still works. To configure replication:

```dotenv
OPENETR_BLOSSOM_SERVERS=https://blossom.example.org,https://backup.example.org
OPENETR_BLOSSOM_REQUIRE=any
OPENETR_BLOSSOM_TIMEOUT_SECONDS=20
OPENETR_BLOSSOM_OPERATION_TIMEOUT_SECONDS=60
```

The plural setting accepts commas or whitespace and overrides the singular one.
Origins must be public HTTPS, without credentials, paths, queries or fragments.
Duplicate origins count once. The storage threshold is `any` (one, default),
`half` (ceiling of N/2), `majority` (floor of N/2 plus one), or `all` (N).
All configured servers are attempted; the threshold is not a replication limit.
If it is unmet, no anchor is published. Some copies may already exist; retrying
checks them before uploading again. These thresholds are local storage policy,
not consensus or retention guarantees. Users who do not select storage can still
publish anchors without Blossom hints.

Upload destinations and retrieval candidates are separate settings:

```dotenv
OPENETR_BLOSSOM_SERVERS=https://storage.example.org
OPENETR_BLOSSOM_QUERY_SERVERS=https://storage.example.org,https://archive.example.org
```

`OPENETR_BLOSSOM_QUERY_SERVERS` accepts commas or whitespace, with
`OPENETR_BLOSSOM_QUERY_SERVERS_FILE` taking precedence when supplied. When unset
(or an empty environment variable), retrieval falls back to the upload pool.
Retrieval combines verified anchor hints, an optional form entry, query servers,
and upload servers into one pool. Stroma normalizes and deduplicates the combined
origins. These are concurrent retrieval candidates, not strict sequential
fallback stages: the first digest-verified copy wins. Each configured pool and
the hint list is bounded to 32 origins, allowing up to 97 unique retrieval
candidates including the form entry, with four concurrent requests and the
existing overall deadline.
Query servers, anchor hints, and per-query form entries never become upload
destinations. `OPENETR_BLOSSOM_REQUIRE` applies only to uploads.

Public QR lookups combine query and upload servers with permitted hints from
signature- and event-ID-verified matching anchors. The first SHA-256-verified
copy suffices. Requests are bounded, private destinations and redirects are
blocked, and only supported PDFs/images are previewed. Verified preview bytes
are cached temporarily, avoiding a second download during page rendering.

Result pages include a branded QR code for public digest lookup. The QR image is served from `/etr/qr/<digest>` as PNG data, and it encodes `<request-base-url>/etr/<digest>` only; the app uses its configured default relays when that URL is opened. The QR generator supports `?encoding=hex` and `?encoding=base64url`. Public `/etr/<digest>` lookup links accept either a 64-character lowercase hexadecimal SHA-256 digest or its equivalent 43-character unpadded Base64URL encoding and normalize both to lowercase hexadecimal before querying OpenETR events. The request base URL honors `Forwarded`, `X-Forwarded-Proto`, and `X-Forwarded-Host` headers for TLS reverse proxy deployments. Set `OPENETR_PUBLIC_BASE_URL` only when deployment should force a different public base URL than the incoming request host.

The result page includes the same categories of information shown by the CLI:

- the Anchor Record and Anchor signer
- matching Anchor Records
- matching control records
- the reconstructed DCR history
- verifier warnings and consequential lifecycle state
- the derived controller

## Docker

The app can also be built and run as a single container.

Build from the repo root so Docker can see both the `openetr` package and the `app/` directory:

```sh
docker build -f app/Dockerfile -t openetr-web .
```

Run it:

```sh
docker run --rm -p 8000:8000 \
  -e OPENETR_APP_SESSION_SECRET=change-me \
  -e OPENETR_ROOT_NSEC=your-root-nsec \
  -e OPENETR_HOME_RELAYS=wss://your-home-relay \
  -e OPENETR_GIT_COMMIT=$(git rev-parse --short HEAD) \
  openetr-web
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## Docker Compose

A simple Compose file is also available at the repo root:

```sh
docker compose up --build
```

It uses the same build context and `gunicorn` entrypoint as the standalone Docker run.

If you want to override the session secret:

```sh
OPENETR_APP_SESSION_SECRET=change-me docker compose up --build
```

For stateless relay-backed operation, also provide the root bootstrap and home relays as environment variables:

```sh
OPENETR_APP_SESSION_SECRET=change-me \
OPENETR_ROOT_NSEC=your-root-nsec \
OPENETR_HOME_RELAYS=wss://your-home-relay \
OPENETR_GIT_COMMIT=$(git rev-parse --short HEAD) \
docker compose up --build
```

If you later move to mounted secrets, the web app and runtime bootstrap also support `_FILE` variants:

```sh
OPENETR_APP_SESSION_SECRET_FILE=/run/secrets/openetr_session_secret OPENETR_ROOT_NSEC_FILE=/run/secrets/openetr_root_nsec OPENETR_HOME_RELAYS_FILE=/run/secrets/openetr_home_relays OPENETR_GIT_COMMIT=$(git rev-parse --short HEAD) docker compose up --build
```

If you change the runtime bootstrap values, restart the service:

```sh
docker compose down
docker compose up --build
```

## Do We Need Docker Compose?

Not strictly.

Right now the web app is still a single service, so the `Dockerfile` is enough for straightforward build and deployment.

Compose is now included mainly for convenience and for future growth. It becomes more useful if you later want to add:

- a reverse proxy
- a separate API container
- local development volumes and overrides
- observability or background workers

## Stateless Runtime Model

The intended container deployment model is stateless:

- no mounted `~/.openetr` directory
- no local `config.yaml` required in the container
- relay-backed profiles, profile config, and signer secrets
- runtime bootstrap supplied by environment variables

For the web app to discover relay-backed profiles and encrypted profile signer records, supply:

- `OPENETR_ROOT_NSEC` or `OPENETR_ROOT_NSEC_FILE`
- `OPENETR_HOME_RELAYS` or `OPENETR_HOME_RELAYS_FILE`

### Record-query relays

The home-page Query DCR form accepts a per-query **Blossom server**, prefilled with
the first configured retrieval origin. It is an additional retrieval candidate
alongside the query pool, upload servers, and verified anchor hints, not an upload
destination.
The uploaded artifact supplies the digest. Retrieval failure does not prevent
record evidence from being shown and does not invalidate the anchor.

Set `OPENETR_QUERY_RELAYS` independently of the home/bootstrap relays:

```dotenv
OPENETR_HOME_RELAYS=wss://home.example.org
OPENETR_QUERY_RELAYS=wss://relay.openetr.org,wss://records.example.org
```

This setting is used for public `/etr/{digest}` lookups (including QR links) and
prepopulates record-query forms in the Control Desk, OpenETR, warehouse receipt,
and product passport pages. Forms and upload-query API requests may explicitly
override it with their `relays` field. `OPENETR_QUERY_RELAYS_FILE` is also supported
and takes precedence over the environment value. Relay entries can be separated
by commas or spaces.

When unset, queries retain the existing browser-session working relays, falling
back to the packaged default (`wss://relay.openetr.org`). A configured query pool
takes precedence over previously saved session defaults. Home relays, Commitment
Profile discovery, publication destinations, and post-publication confirmation
queries are unchanged. This setting applies to the demonstration web app, not CLI
profile defaults.

After deploying this version and editing `.env`, recreate the container with
`docker compose up -d --force-recreate`. Build or pull the updated image first;
restarting an old image does not add support for this setting.

For browser-session encryption, you can also use:

- `OPENETR_APP_SESSION_SECRET` or `OPENETR_APP_SESSION_SECRET_FILE`

The browser session may still hold the logged-in `nsec` in an encrypted cookie for this demo app, but the container itself does not rely on local profile or session files.
