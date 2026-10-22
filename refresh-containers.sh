#!/bin/sh
set -eu
repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$repo_dir"

health_timeout=120
case "$#:${1:-}" in
    0:) ;;
    1:-h|1:--help) printf '%s\n' 'Usage: ./refresh-containers.sh [--timeout SECONDS] (default: 120; readiness wait excludes build time)'; exit 0 ;;
    2:--timeout) health_timeout=$2 ;;
    *) printf '%s\n' 'Usage: ./refresh-containers.sh [--timeout SECONDS]' >&2; exit 2 ;;
esac
case "$health_timeout" in
    ''|0*|*[!0-9]*) printf '%s\n' 'Timeout must be an integer from 1 to 3600 seconds.' >&2; exit 2 ;;
esac
if [ "${#health_timeout}" -gt 4 ] || [ "$health_timeout" -gt 3600 ]; then
    printf '%s\n' 'Timeout must be an integer from 1 to 3600 seconds.' >&2
    exit 2
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
    printf '%s\n' 'Tracked working-tree changes are present; review and preserve them before refreshing. Keep deployment storage paths in .env; do not stash storage changes just to bypass this check.' >&2
    exit 1
fi
if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
    printf '%s\n' 'Docker with the Compose plugin is required.' >&2
    exit 1
fi
if ! docker info >/dev/null 2>&1; then
    printf '%s\n' 'Docker is unavailable; check that it is running and your user has access.' >&2
    exit 1
fi
if ! docker compose up --help | grep -q -- '--wait-timeout'; then
    printf '%s\n' 'Update Docker Compose: --wait and --wait-timeout support is required.' >&2
    exit 1
fi

printf '%s\n' 'Pulling fast-forward changes...'
git pull --ff-only

printf '%s\n' 'Validating Docker Compose configuration...'
docker compose config --quiet

startup_failed() {
    printf '%s\n' "$1" >&2
    docker compose ps --all web >&2 || true
    for service in web; do
        containers=$(docker compose ps --all --quiet "$service") || continue
        for container in $containers; do
            printf '%s\n' "Diagnostics for $service ($container):" >&2
            docker inspect --format '{{.State.Status}} exit={{.State.ExitCode}} oom={{.State.OOMKilled}} error={{.State.Error}}' "$container" >&2 || true
            docker inspect --format '{{if .State.Health}}{{range .State.Health.Log}}health exit={{.ExitCode}}: {{.Output}}{{end}}{{end}}' "$container" >&2 || true
        done
    done
    docker compose logs --no-color --tail=100 web >&2 || true
    exit 1
}

printf '%s\n' 'Building container images...'
if ! docker compose build; then
    startup_failed 'Image build failed; containers were not recreated.'
fi
printf '%s\n' "Recreating services and waiting up to ${health_timeout}s for readiness..."
if ! docker compose up --force-recreate --detach --wait --wait-timeout "$health_timeout"; then
    startup_failed "Startup failed or services did not become healthy within ${health_timeout}s."
fi
docker compose ps
printf '%s\n' 'Required services passed their readiness checks. Verify public access and application workflows separately.'
