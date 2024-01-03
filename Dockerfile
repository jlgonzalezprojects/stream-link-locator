FROM python:3.9-slim-bullseye

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.2 \
  PORT=9000

RUN pip install "poetry==$POETRY_VERSION" \
    && apt-get -q update \
    && apt-get install --no-install-recommends -yq postgresql-client-13 gcc musl-dev build-essential python3-dev libghc-hdbc-postgresql-dev

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
COPY . /code

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

EXPOSE $PORT

CMD ["uvicorn", "stream_link_locator.entrypoints.fastapi_app:app", "--host", "0.0.0.0", "--port", "9000"]