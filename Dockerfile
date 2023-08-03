FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY . .

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

WORKDIR src/
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "config.wsgi", "access-logfile", "-"]
