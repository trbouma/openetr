# Multi-Modality Architecture Note

This note describes the implementation methodology for OpenETR as a single core system delivered through four modalities:

- a web application for human use
- a CLI for human use
- a CLI for agent use
- an API for agent use

The purpose of this note is not to freeze a final code structure.

Its purpose is to define the architectural direction that should guide ongoing refactoring and feature development.

## Status

Draft.

## Objective

OpenETR should behave as one system with multiple delivery surfaces, not as several independent applications that happen to share a repository.

That means the business logic for querying, issuing, transferring, validating, and publishing should live in the `openetr` module, while each delivery surface should be a thin adapter around that shared core.

The goal is equivalence of behavior across modalities, with differences only where the interaction model requires them.

The same OpenETR component should also be usable in two integration styles:

- embedded directly into another application runtime, where the host application imports and calls `openetr` services;
- exposed by a running OpenETR instance, where another system calls REST APIs over HTTP.

Both styles should route through the same object/service layer.

## The Four Modalities

### 1. Web Application

The web application exists for interactive human use.

Its responsibilities are:

- collect input through forms and navigation
- manage session state
- present results in HTML
- present warnings and confirmations as pages

It should not become the place where core OpenETR rules are reimplemented.

The preferred web application style is hypermedia-first.

OpenETR web flows should follow a HATEOAS-oriented philosophy:

- server-rendered pages and fragments represent the current application state
- forms and links express the actions that are available from that state
- the server returns the next useful representation after each action
- client-side JavaScript is kept to a minimum
- htmx may be used to improve responsiveness while preserving ordinary HTML form semantics

In this model, htmx is a progressive enhancement over server-rendered HTML, not a separate client application. A profile switch, issue action, query, transfer, or confirmation should still be understandable as a form submission or link traversal. The browser may update a page fragment in place, but the state transition remains owned by the server and the shared `openetr` services.

### 1a. Web REST/API Mode

The same running web application may also expose REST-style endpoints for agents, scripts, services, and external product systems.

Its responsibilities are:

- accept structured requests, including uploads, object identifiers, profile references, and control-action parameters
- return structured JSON responses
- surface guard warnings, confirmation requirements, and policy failures as machine-readable results
- preserve the same OpenETR behavior used by the human web pages

The REST/API mode should be understood as an adapter over the OpenETR component, not as a separate policy implementation.

### 2. CLI for Human Use

The human CLI exists for operators, testers, and developers who want direct terminal workflows.

Its responsibilities are:

- parse command-line options
- prompt for confirmation where needed
- render readable terminal output
- provide operator-friendly warnings and diagnostics

It should remain friendly and expressive, but should rely on shared `openetr` services for the actual workflow semantics.

### 3. CLI for Agent Use

The agent CLI exists for deterministic invocation by scripts, agents, orchestration systems, and automated pipelines.

Its responsibilities are:

- accept explicit machine-oriented arguments
- avoid interactive prompts unless explicitly enabled
- return stable, structured output
- expose failure conditions clearly and predictably

This does not necessarily require a completely separate executable.

The preferred approach is that the existing CLI supports an agent-oriented mode through flags such as:

- `--json`
- `--no-input`
- `--confirm`
- `--quiet`

In the current implementation, `--json` is the primary boundary for agent-friendly command output. Commands using `--json` should return structured success, warning, confirmation-required, and error responses rather than human-only terminal text.

### 4. API for Agent Use

The API exists for programmatic use over HTTP.

Its responsibilities are:

- accept structured requests
- return structured JSON responses
- expose the same guard and validation semantics as the CLI
- provide stable request and response shapes suitable for automation

The API should not diverge semantically from the CLI and web app.

## Runtime And Service Integration

OpenETR can be integrated in two complementary ways.

### Embedded Component

An application runtime can import the OpenETR component and call its service layer directly.

This is useful when the host application wants OpenETR behavior inside its own process, account model, job queue, transaction logging, custody model, or workflow engine.

In this mode, the host application supplies its own surrounding concerns:

- user authentication
- authorization
- tenant or organization structure
- UI and workflow
- storage caches or indexes
- domain-specific policy selection

The OpenETR component supplies the control-layer behavior:

- digest and object-id handling
- identifier resolution
- baseline or custom guard evaluation
- event construction
- signing
- relay publication and query
- verifier result construction

### Running OpenETR Service

An application may instead call a running OpenETR instance over REST APIs.

This is useful when the host system is not Python-based, wants a process boundary, wants centralized relay/profile management, or wants a shared OpenETR service for several applications.

In this mode, the OpenETR service acts as an HTTP adapter over the same component.

The integration choice is therefore:

```text
host app imports openetr
        or
host app calls OpenETR REST API
        ↓
same OpenETR component/service layer
        ↓
canonical identifiers
baseline or custom policy guards
signed event publish/query
structured verifier output
```

## Core Architectural Principle

The governing principle is:

> One domain core, multiple adapters.

In OpenETR, the `openetr` package should become the application core.

That core should own:

- digest and object-identifier handling
- relay interactions
- signer resolution
- profile resolution
- guard evaluation
- issue, query, transfer, and profile-publish workflows
- result construction
- validation and policy semantics

The adapters should own only the modality-specific concerns.

In compact form:

```text
Human web UI
Agent REST/API
Human CLI
Agent CLI with --json
Embedded application runtime
        ↓
OpenETR component/service layer
        ↓
identifier resolution
baseline or custom policy guards
event construction / query
verification / structured result
```

## What Belongs in `openetr`

The `openetr` module should contain reusable services or use cases for operations such as:

- `query_etr`
- `issue_etr`
- `publish_profile`
- `transfer_initiate`
- `transfer_accept`
- `transfer_terminate`
- `evaluate_issue_guard`
- `evaluate_transfer_guard`

These services should return structured results rather than printing directly.

That allows:

- the web app to render HTML
- the human CLI to render readable text
- the agent CLI to emit JSON
- the API to return JSON

without changing the underlying behavior.

## What Belongs in Adapters

### Web Adapter

The web app should handle:

- routes
- session cookies
- form parsing
- Jinja templates
- browser-oriented confirmation flows
- hypermedia controls, including links, forms, and htmx-enhanced fragments

### Human CLI Adapter

The human CLI should handle:

- `click` parsing
- terminal prompts
- human-readable formatting
- operator-facing warnings

### Agent CLI Adapter

The agent CLI should handle:

- machine-friendly flags
- non-interactive execution
- structured serialization
- explicit exit semantics

### API Adapter

The API should handle:

- HTTP routing
- request validation
- authentication or session policy as needed
- JSON response serialization

## Equivalent Semantics Across Modalities

The four modalities should not invent separate rules.

They should share:

- the same validation guards
- the same object lookup rules
- the same profile-merge rules
- the same transfer resolution logic
- the same current-controller or current-title determination
- the same warning conditions

Where interaction differs, the semantics should remain the same while the presentation changes.

For example:

- human CLI warning: interactive terminal confirmation
- web warning: confirmation page
- agent CLI warning: structured guard result and non-zero exit unless explicitly confirmed
- API warning: structured response indicating confirmation is required

The user experience changes.

The rule does not.

## Structured Results as the Boundary

To make this architecture work, shared services should return structured result objects.

Examples include:

- query results
- publish results
- guard results
- control-event validation results
- profile publish results

These may initially be dictionaries.

Over time, OpenETR should consider moving toward explicit dataclasses or Pydantic models for stronger contracts and easier reuse across CLI, web, and API layers.

## Root Key Separation

OpenETR should maintain a strict separation between the administrative root key and operational profile identities.

The `root_nsec` is intended to manage relay-backed configuration and profile control data, including:

- the relay-backed profiles index
- relay-backed profile configuration records
- relay-backed encrypted profile signer secrets

It is not intended to act as a public-facing user identity.

As a design rule, the root key should:

- not publish a profile
- not serve as an operational signer for normal ETR workflows
- not be treated as a user-facing identity in the web app or CLI

The purpose of this separation is to reduce attack surface and preserve cleaner key hygiene.

Operational profile signers may publish profiles and perform public or transactional actions.

The root key should remain an administrative control and recovery key only.

## Web Login Semantics

The web app should distinguish between:

- recovery of an existing relay-backed identity
- creation of a brand-new identity

The intended semantics are:

- `Login with nsec`
  This is a recovery path for an existing relay-backed identity.
  The supplied `nsec` should only be accepted when the selected bootstrap relay set can actually recover relay-backed configuration for that root identity.

- `Generate New nsec`
  This is a creation path for a brand-new identity.
  The app may generate a fresh root key, establish the browser session, and begin using the selected bootstrap relay set for new relay-backed state.

This distinction avoids treating every arbitrary `nsec` as an already valid OpenETR root identity.

It also preserves an important operational boundary:

- manual login means “recover an existing identity”
- generated login means “bootstrap a new identity”

The browser session may retain session-local state such as the currently selected profile, but successful recovery of durable state should depend on relay-backed configuration discoverable from the root key and bootstrap relay set.

## Recommended Repository Shape

The following direction is recommended:

- `openetr/`
  The domain and application core.
- `openetr/services/`
  Shared workflows and service-layer logic.
- `openetr/commands/`
  Human CLI adapters built on top of services.
- `app/`
  Human-oriented FastAPI and Jinja web application.
- `app/routers/` or similar
  JSON API routes for agent use when the API surface grows.
- `docs/specs/`
  Design notes, protocol notes, and architecture notes such as this one.

This note does not require the repository to be rearranged immediately.

It defines the intended direction for future refactoring.

## Methodology for New Features

New features should be developed in the following order whenever practical:

1. Define or refine the workflow in `openetr`.
2. Return a structured result from that workflow.
3. Adapt that shared workflow to the human CLI.
4. Adapt the same workflow to the web app.
5. Expose the same workflow through agent-oriented CLI or API surfaces.

This order helps prevent presentation layers from becoming the de facto source of business logic.

## Current Refactoring Direction

The repository has already begun moving in this direction.

Examples include:

- shared query logic in `openetr.services.query_etr`
- shared issue guard logic in `openetr.guards`
- shared issue publish logic in `openetr.services.issue_etr`
- shared profile publish logic in `openetr.services.profile_publish`

This direction should continue until the major workflows are owned by `openetr` and the adapters become progressively thinner.

## Human vs Agent Experience

The human and agent modalities should differ primarily in ergonomics, not in substantive behavior.

Human-oriented surfaces should prefer:

- richer explanatory text
- prompts and confirmations
- visually readable output

Agent-oriented surfaces should prefer:

- stable schemas
- deterministic output
- explicit status handling
- prompt-free execution by default

This distinction is important because it allows OpenETR to support both operator usability and automation reliability without splitting the domain logic into parallel implementations.

## Design Significance

OpenETR is intended to operate as an open system rather than a closed platform.

That makes consistency across modalities especially important.

If the web app, CLI, API, and agent flows disagree about what an operation means, the system becomes harder to trust, harder to test, and harder to evolve.

By concentrating the logic in `openetr`, OpenETR can:

- reduce duplication
- reduce semantic drift
- improve testability
- support automation more safely
- preserve consistent behavior across human and machine interfaces

## Working Rule

The working rule for future development should be:

> If a rule matters to more than one modality, it belongs in `openetr`.

That rule should guide both feature implementation and ongoing refactoring.
