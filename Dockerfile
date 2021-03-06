# https://hub.docker.com/_/python?tab=description
FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG 0
ENV CTFPAD_HOSTNAME localhost                # change here if publicly exposed
ENV HEDGEDOC_URL http://hedgedoc:3000        # change here if publicly exposed
ENV WHITEBOARD_URL http://whiteboard:8080    # change here if publicly exposed

WORKDIR /code
COPY requirements.txt .

RUN \
 apt-get update && \
 apt-get upgrade -y && \
 apt-get install -y libpq-dev python3-dev postgresql-client && \
 python3 -m pip install --upgrade pip && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apt-get autoclean && \
 apt-get autoremove


COPY . .

ENTRYPOINT ["bash", "/code/docker-entrypoint.sh"]
