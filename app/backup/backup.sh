#!/bin/sh
set -eu

BACKUP_DIR="${BACKUP_DIR:-/backups}"
RETENTION="${BACKUP_RETENTION:-10}"
TIMESTAMP="$(date -u +%Y%m%d_%H%M%S)"
BACKUP_FILE="${BACKUP_DIR}/namo_${TIMESTAMP}.dump"

mkdir -p "$BACKUP_DIR"

if [ -f /run/secrets/prod_postgres_password ]; then
  PGPASSWORD="$(cat /run/secrets/prod_postgres_password)"
else
  echo "Missing /run/secrets/prod_postgres_password" >&2
  exit 1
fi

export PGPASSWORD

pg_dump \
  -h "${DATABASE_HOST:?}" \
  -U "${POSTGRES_USER:?}" \
  -d "${POSTGRES_DB:?}" \
  -Fc \
  -f "$BACKUP_FILE"

if [ ! -s "$BACKUP_FILE" ]; then
  echo "Backup failed: empty file" >&2
  exit 1
fi

# Keep only the newest N backups.
ls -1t "${BACKUP_DIR}"/namo_*.dump 2>/dev/null | tail -n +"$((RETENTION + 1))" | xargs -r rm -f
