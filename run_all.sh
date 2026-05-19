#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if command -v docker-compose >/dev/null 2>&1; then
  echo "Ejecutando: docker-compose up --build"
  docker-compose up --build
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  echo "Ejecutando: docker compose up --build"
  docker compose up --build
else
  echo "ERROR: no se encontró docker-compose ni docker compose. Instala Docker Compose o usa Docker 20.10+ con el plugin compose."
  exit 1
fi
