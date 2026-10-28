# Koyeb + Neon

Django package: `nyondo_stock`; application directory: `nyondo_stock/`.
Use Koyeb's Python buildpack with work directory `nyondo_stock` and Python 3.13.15
(pinned in `.python-version`). Expose HTTP port 8000 and route `/` to it.

Build command: `bash build.sh`
Run command: `gunicorn nyondo_stock.wsgi:application --bind 0.0.0.0:${PORT:-8000}`
Set `PORT=8000` to match the exposed port.

Set these variables in Koyeb (make credentials secrets):
- `SECRET_KEY`: a new, long random Django secret; required at build and runtime.
- `DATABASE_URL`: Neon PostgreSQL connection URL with `sslmode=require`;
  retain the SSL parameters provided by Neon. Required at build and runtime.
- `DEBUG=False` (also the default).
- `ALLOWED_HOSTS`: comma-separated exact Koyeb hostname and any custom domains,
  without schemes or paths.
- `CSRF_TRUSTED_ORIGINS`: comma-separated HTTPS origins with schemes,
  e.g. `https://your-app.koyeb.app` and any custom domain origins.
- `PORT=8000`.

`dj-database-url`, `psycopg2-binary`, Gunicorn and WhiteNoise already exist in
requirements.txt. WhiteNoise uses Django's current STORAGES setting.
Koyeb's KOYEB_SERVICE_NAME triggers a missing-DATABASE_URL configuration error.

Before serving traffic, explicitly run `python manage.py migrate` once in the
production environment against the intended Neon database. The build does not
run migrations. No migrations were run during preparation. Back up existing
data before planning any transfer; local SQLite data is not copied to Neon.

For local development, keep the existing .env private, set SECRET_KEY and
DEBUG=True, and optionally omit DATABASE_URL to use the existing SQLite DB.
Run commands from nyondo_stock/. To retain Render, set its host and HTTPS origin
in ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS on Render as well.

The local .env, SQLite database and private Readme were removed from Git tracking
without deleting the files. They can still exist in earlier commits: rotate any
previously tracked secrets, database credentials and listed login passwords
before deployment. This change does not rewrite Git history.

Validate the full pinned requirements installation on the Linux build platform.
Uploaded files, if introduced, need durable external storage; Koyeb instance
filesystems are ephemeral. A live Neon connection and Linux Gunicorn launch
must still be verified during deployment.

## Preparation verification

settings.py passed Python syntax parsing. Both requested commands were attempted:
`python manage.py check` and `python manage.py collectstatic --noinput`.
Both stopped with ModuleNotFoundError: django. System and bundled Python lack
Django; installing requirements into an isolated check environment failed because
shell connections to PyPI were blocked despite a network permission grant.
The existing project venv was not accessed or modified. Rerun both commands in a
provisioned environment before deployment. Static manifest generation, full pinned
dependency installation, and live Neon connectivity remain unverified.


## Neon CLI setup (2026-10-28)

The repository is linked locally to project `old-butterfly-92432077`, branch
`production`, organization `org-solitary-firefly-93806107`. `neon.ts` declares
Postgres-only usage. Run `npx neon@latest deploy` to reconcile it and pull the
branch environment. The local `.neon` link and environment files are ignored.

Django loads repository-root `.env.local` and `.env` before application-directory
env files; process environment variables take priority. The existing Django ORM,
`dj-database-url` and `psycopg2-binary` use `DATABASE_URL` for application traffic.
Use `DATABASE_URL_UNPOOLED` as `DATABASE_URL` in the migration process for direct
schema operations; do not replace the application's pooled connection permanently.

Install Python requirements into `.venv` at the repository root. `npm run build`
uses that environment (or `PYTHON`, if set) to run Django checks and collect static
assets. `npm start` runs the local development server at http://127.0.0.1:8000/.
Production continues to use the Gunicorn command above.

With the local server running, run `.venv\Scripts\python.exe scripts/verify_neon.py`
on Windows (`.venv/bin/python scripts/verify_neon.py` on Linux). It verifies Neon
connectivity, HTTP login, database-backed sessions, the manager dashboard, and
category create/read/update/delete through HTTP. It creates a temporary manager
account and category and removes its test records in a finally block.

The initial 44 Django migrations were applied successfully to the empty Neon
production database using the direct connection. Existing local/Render inventory
and user records were not transferred.
