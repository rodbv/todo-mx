run:
    uv run python manage.py runserver_plus

test:
    uv run ptw .

migrate:
    uv run python manage.py migrate

csu:
    uv run python manage.py createsuperuser

makemigrations:
    uv run python manage.py makemigrations

ppaliases:
    mm: makemigrations
    t: test
    r: run
    mi: migrate