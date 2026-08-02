# Blue Sky Money Transfer

Django rewrite of the Blue Sky money transfer website, built to run on PythonAnywhere (Python-only hosting — no Node.js server, no Prisma).

## Stack

- Django 5.2 LTS, MySQL (PythonAnywhere-hosted) in production, SQLite for local dev
- Tailwind CSS v4, compiled locally to a static `output.css` (Node is only ever used at build time, never on the server)
- Vanilla JS for dark mode and the 3D tilt/glare card effect (`static_src/js/`)

## Local development

```bash
python -m venv .venv
source .venv/Scripts/activate      # Windows Git Bash
pip install -r requirements.txt
cp .env.example .env                # defaults to SQLite, no MySQL needed locally
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

To rebuild the CSS after changing templates or `static_src/css/input.css`:

```bash
npm install
npm run build:css
```

## Project layout

- `config/` — settings, root URLconf, WSGI
- `core/` — shared base template, static site content (`core/data.py`), icon/UI template tags, decorators
- `accounts/` — custom email-based `User` model, signup/login/logout
- `marketing/` — public pages (home, à propos, équipe, impact, pays, contact) + `ContactMessage`
- `transfers/` — dashboard: `Recipient`, `Transfer` models, views, forms
- `static_src/` — source CSS/JS/images (Tailwind input, vanilla JS, photos)
- `staticfiles/` — `collectstatic` output (gitignored, generated)

## Deploying to PythonAnywhere

1. **Upload the code** — clone the repo into your PythonAnywhere account (Bash console: `git clone ...`).
2. **Virtualenv** — in a Bash console:
   ```bash
   mkvirtualenv --python=python3.12 bluesky-env
   pip install -r requirements.txt
   ```
3. **Database** — create a MySQL database from the *Databases* tab. Note the host/user/password shown there.
4. **Environment variables** — on the *Web* tab, add environment variables (or create `.env` in the project root):
   `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=<yourusername>.pythonanywhere.com`, `DB_ENGINE=mysql`, `DB_NAME=<yourusername>$bluesky`, `DB_USER=<yourusername>`, `DB_PASSWORD=...`, `DB_HOST=<yourusername>.mysql.pythonanywhere-services.com`, `DB_PORT=3306`.
5. **Migrate**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. **Static files** — build the CSS locally first (`npm run build:css`, commit `static_src/css/output.css`), then on PythonAnywhere:
   ```bash
   python manage.py collectstatic --noinput
   ```
   On the *Web* tab, add a static files mapping: URL `/static/` → Directory `/home/<yourusername>/<project>/staticfiles`.
7. **WSGI file** — edit the auto-generated WSGI file under the *Web* tab's Code section so it points at `config.wsgi.application` (see the Django section of that file — uncomment and adjust the `sys.path` and `DJANGO_SETTINGS_MODULE`).
8. **Reload** the web app from the *Web* tab.
