# django-survey-app

[![CI](https://github.com/Wil12Fred/django-survey-app/actions/workflows/ci.yml/badge.svg)](https://github.com/Wil12Fred/django-survey-app/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Django REST Framework API for building surveys — free-text, single-choice
and ranking questions — collecting answers anonymously and reporting on them:
top words, the share of each option, and the distribution of ranks.

## Features

- Model (Spanish names): `Alternativa` (an option), `Pregunta` (a question,
  `tipo` 0 = free text, 1 = single choice, 2 = ranking), `Pregunta_detalle`
  (links an option to a question, once), `Encuesta` (a survey),
  `EncuestaPregunta` (places a question in a survey).
- Answers, open to anonymous users:
  - text (`/api/solucion_texto_detalle/`) — split into words and counted per
    question in `Solucion_texto`; refused for a non-text question;
  - single choice (`/api/solucion_alternativa_detalle/`) — refused for a
    non-choice question;
  - ranking (`/api/alternativa_orden/`) — a position from 1 to the number of
    options, for an option of that question; repeated answers add to a total.
- `GET /api/reporte=<id>/detail` — per question of the survey: the 50 most
  frequent words, the share of each option, or for each option the share of
  each rank.
- Hyperlinked resources (`/api/<resource>=<id>/detail`); creating surveys,
  questions and options needs a JWT (`Authorization: JWT <token>`), reading is
  public. Registration and JWT login through djoser, by username or e-mail.
  Swagger UI at `/`.

## Requirements

- Python 3.10–3.12 and [uv](https://docs.astral.sh/uv/).
  - Debian/Ubuntu: `sudo apt install python3`, then
    `curl -LsSf https://astral.sh/uv/install.sh | sh` (uv is not packaged).
  - Arch: `sudo pacman -S python uv`
- Optional: PostgreSQL for the `production` settings
  (`postgresql` on both; `uv sync --extra postgres`).

`DJANGO_SECRET_KEY` overrides the development key (see `.env.example`); the
settings module is chosen in `backend/config/environment.py`.

## Build

```bash
cd backend
uv sync --locked
uv run python manage.py check
```

## Run

```bash
cd backend
uv run python manage.py migrate        # SQLite, creates backend/db.sqlite3
uv run python manage.py runserver      # http://127.0.0.1:8000
```

Captured from a real run (register and get a token first, as in
`POST /auth/users/create/` and `POST /auth/jwt/create/`):

```
$ curl -H "Authorization: JWT <token>" -H 'Content-Type: application/json' \
    -d '{"nombre":"Habitos","descripción":"demo"}' http://127.0.0.1:8000/api/encuesta/
{"url":"http://127.0.0.1:8000/api/encuesta=1/detail","nombre":"Habitos","fecha":"2026-11-26","descripción":"demo","preguntas":[]}
# ... a text question placed in the survey, then two anonymous answers,
#     "mucho cafe" and "cafe negro"
$ curl http://127.0.0.1:8000/api/reporte=1/detail
{"http://127.0.0.1:8000/api/encuesta=1/detail":{"http://127.0.0.1:8000/api/encuesta_pregunta=1/detail":{"problema":"http://127.0.0.1:8000/api/pregunta=1/detail","textos":{"cafe":2,"mucho":1,"negro":1}}}}
```

## Tests

```bash
cd backend
uv run python manage.py test          # 15 tests, SQLite
```

- `encuesta/tests.py` — anonymous users cannot create a survey; a
  single-choice survey with four answers reports 0.75 / 0.25; a text answer
  is refused for a choice question.
- `encuesta/test_api.py` — option detail returns that option; a question
  lists its options; `tipo` outside 0–2 and a duplicate option link are
  refused; a survey lists its questions and can be renamed; anonymous users
  read but cannot create; text answers are counted per word; a choice answer
  is refused for a text question; ranking answers are aggregated and their
  shares reported; out-of-range positions and options of another question are
  refused; the report covers every question of a survey; a missing survey
  gives 400.

CI also runs `manage.py check` and `makemigrations --check`.

## Project layout

```
backend/
  config/       settings (base/local/development/production), urls,
                py312_compat.py (six shim for Django 2.2 on Python 3.12)
  custom_user/  User model that logs in by username or e-mail
  encuesta/     survey models, serializers, views and report, tests
```

## Known limitations

- **Pinned old stack**: Django 2.2 (end of life), DRF 3.9, djoser 1.x and the
  unmaintained `djangorestframework-jwt`, kept because djoser 1.x does not run
  on Django 3+; `config/py312_compat.py` and `setuptools<81` keep it working
  on Python 3.12.
- No frontend; the API is exercised with curl or the Swagger UI.
- A single-choice answer is not checked against the question's options (the
  report just ignores a foreign option), and the same person can answer any
  number of times.
- Words in text answers longer than 30 characters do not fit `Solucion_texto`.
- `Solucion_alternativa_orden_detalle` / `Encuesta_alternativa_orden` are
  modelled and routed but not used by the report.
- A `db.sqlite3` left from 2019 (it used to be committed) holds rows with
  dangling foreign keys and does not migrate: delete it first.

## Background

Written in 2019 as a take-home exercise, reusing the backend skeleton of
[django-react-library](https://github.com/Wil12Fred/django-react-library)
(custom user, djoser registration, JWT login). That repository's unused
`library` and `pago` apps were copied along and have since been removed.

## License

MIT — see [LICENSE](LICENSE).
