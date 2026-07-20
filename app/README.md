# Demo App

This directory contains a demonstration FastAPI app that is intentionally kept separate from the installable `openetr` component.

## Separation Rationale

The root Poetry package defines `openetr` as the installable component. Files and dependencies under `app/` do not become part of that component unless the root packaging configuration is explicitly changed.

This keeps:

- the reusable `openetr` package clean
- FastAPI and app-only dependencies out of the core component
- the demo web app free to evolve independently

## Install

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

Uploads are limited to 10 MiB by default. Set `OPENETR_MAX_UPLOAD_BYTES` to override the limit for a deployment.

When the uploaded file is a PDF or supported image, the result page also shows an inline preview. Preview files are temporary, tokenized, served with `Cache-Control: no-store`, and cleaned up after one hour. PDFs render through the bundled PDF.js assets under `app/assets/js`.

Issue upload forms can optionally store the raw uploaded file on the app-managed Blossom server so later QR lookups can retrieve the document by digest. Blossom uploads are authorized with a short-lived signed Nostr event from the issuing signer. The default Blossom server is `https://blossom.getsafebox.app`. Set `OPENETR_BLOSSOM_SERVER` to use a different server, and `OPENETR_BLOSSOM_TIMEOUT_SECONDS` to adjust storage request timeouts. Public digest lookup pages verify Blossom bytes against the requested SHA-256 digest before rendering supported PDFs or images.

Result pages include a branded QR code for public digest lookup. The QR image is served from `/etr/qr/<digest>` as PNG data, and it encodes `<request-base-url>/etr/<digest>` only; the app uses its configured default relays when that URL is opened. The request base URL honors `Forwarded`, `X-Forwarded-Proto`, and `X-Forwarded-Host` headers for TLS reverse proxy deployments. Set `OPENETR_PUBLIC_BASE_URL` only when deployment should force a different public base URL than the incoming request host.

The result page includes the same categories of information shown by the CLI:

- the initial ETR origin event
- issuer profile details
- matching origin records
- matching control events
- the summary control chain
- the current controller

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

For browser-session encryption, you can also use:

- `OPENETR_APP_SESSION_SECRET` or `OPENETR_APP_SESSION_SECRET_FILE`

The browser session may still hold the logged-in `nsec` in an encrypted cookie for this demo app, but the container itself does not rely on local profile or session files.
