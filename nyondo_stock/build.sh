#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
# Apply migrations separately against the intended production database.
