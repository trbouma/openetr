#!/bin/sh

set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$repo_dir"

printf '%s\n' 'Pulling the latest changes...'
git pull

printf '%s\n' 'Building OpenETR container image...'
docker compose build

printf '%s\n' 'Recreating OpenETR container...'
docker compose up --force-recreate --detach

printf '%s\n' 'OpenETR container refreshed.'
docker compose ps

printf '%s\n' 'Waiting for the OpenETR health check...'
attempt=1
max_attempts=30
while ! docker compose exec -T web python -c \
    "import json, urllib.request; response = json.load(urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)); assert response.get('status') == 'ok'" \
    >/dev/null 2>&1
do
    if [ "$attempt" -ge "$max_attempts" ]; then
        printf '%s\n' 'OpenETR health check failed after 60 seconds.' >&2
        docker compose ps >&2
        exit 1
    fi
    attempt=$((attempt + 1))
    sleep 2
done

printf '%s\n' 'OpenETR health check passed: status=ok'
