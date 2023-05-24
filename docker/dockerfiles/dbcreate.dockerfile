FROM python:3.8

# Var from secrets.env
ARG PG_PASSWORD
ARG PG_USER
ARG PG_DB_NAME
ARG PG_DB_PORT
ARG REDIS_PASSWD
ARG API_TOKEN

ENV POSTGRESS_USER ${PG_USER}
ENV POSTGRESS_PASSWORD ${PG_PASSWORD}
ENV POSTGRESS_DB_NAME ${PG_DB_NAME}
ENV POSTGRESS_DB_PORT ${PG_DB_PORT}
ENV REDIS_PASSWORD ${REDIS_PASSWD}
ENV TG_BOT_TOKEN ${API_TOKEN}

# Build app
WORKDIR /app
COPY ./dbcreate/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./appdb/ ./appdb/
COPY ./dbcreate/ .

# Run app
CMD [ "python3", "./main.py" ]
