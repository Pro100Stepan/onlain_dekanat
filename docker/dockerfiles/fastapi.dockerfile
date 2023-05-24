FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ADD ./source/fastapi_gino_uvicorn/src/database.py ./
CMD [ "python3.8","database.py" ]

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Var from secret.env

ARG PG_PASSWORD
ARG PG_USER
ARG PG_DB_NAME
ARG PG_DB_PORT

ENV POSTGRESS_USER ${PG_USER}
ENV POSTGRESS_PASSWORD ${PG_PASSWORD}
ENV POSTGRESS_DB_NAME ${PG_DB_NAME}
ENV POSTGRESS_DB_PORT ${PG_DB_PORT}

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app/

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./source/fastapi_gino_uvicorn/pyproject.toml ./poetry.lock* ./

COPY ./source/fastapi_gino_uvicorn/alembic.ini ./

COPY ./source/fastapi_gino_uvicorn/scripts/prestart.sh ./
RUN chmod +x prestart.sh

COPY ./source/fastapi_gino_uvicorn/migrations ./migrations/

RUN poetry install --no-root --no-dev

COPY ./source/fastapi_gino_uvicorn/src ./


COPY ./source/appdb/* ./models/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
