# django-survey-app

> Encuesta — survey REST API

A Django REST Framework API for building surveys and reporting on their
answers, written in 2019 as a take-home exercise. It reuses the
backend skeleton of [Django-React](../Django-React) (custom user, djoser
registration, JWT login); there is no frontend.

## Model

- `Alternativa` — an answer option; `Pregunta` — a question with
  `tipo` 0 = free text, 1 = single choice, 2 = ranking; `Pregunta_detalle`
  links options to a question.
- `Encuesta` — a survey; `EncuestaPregunta` places a question in a survey.
- Answers: `Solucion_texto(_detalle)` (text, with counts),
  `Solucion_alternativa_detalle` (chosen option), `Alternativa_orden` (rank).
- `GET /api/reporte=<id>/detail` returns, per question, the top text answers,
  the share of each option, or the rank distribution.

All resources are hyperlinked (`/api/<resource>=<id>/detail`). Reading is
public; writing needs a JWT (`Authorization: JWT <token>`). Swagger UI is at `/`.

## Run

Requires [uv](https://docs.astral.sh/uv/) and Python 3.10–3.12.

```bash
cd backend
uv sync
uv run python manage.py migrate        # SQLite, creates backend/db.sqlite3
uv run python manage.py runserver      # http://127.0.0.1:8000
uv run python manage.py test
```

A `db.sqlite3` left from 2019 (it used to be committed) holds rows with
dangling foreign keys and does not migrate: delete it first.

Example (real output):

```
$ curl -X POST -H 'Content-Type: application/json' \
    -d '{"username":"demo","email":"demo@example.com","password":"S3cure-demo-pw"}' \
    http://127.0.0.1:8000/auth/users/create/
{"email":"demo@example.com","username":"demo","id":1}
$ curl -X POST ... /auth/jwt/create/        -> {"token": "..."}
$ curl -H "Authorization: JWT <token>" -H 'Content-Type: application/json' \
    -d '{"nombre":"Habitos","descripción":"demo"}' http://127.0.0.1:8000/api/encuesta/
{"url":"http://127.0.0.1:8000/api/encuesta=1/detail","nombre":"Habitos","fecha":"2026-11-26","descripción":"demo","preguntas":[]}
```

`encuesta/tests.py` builds a full single-choice survey with four answers and
checks the report returns 0.75 / 0.25.

Stack: Django 2.2 + DRF 3.9 + djoser 1.x + djangorestframework-jwt, pinned in
`backend/pyproject.toml`; `config/py312_compat.py` lets Django 2.2's bundled
`six` work on Python 3.12. `DJANGO_SECRET_KEY` overrides the development key.

## Layout

```
backend/
  config/       settings (base/local/development/production), urls
  custom_user/  User model that logs in by username or e-mail
  encuesta/     survey models, serializers, views, report, tests
  library/, pago/   leftovers from Django-React, not installed
```
