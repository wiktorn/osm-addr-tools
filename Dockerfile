FROM python:3-slim

COPY . /app


RUN cd /app && \
    apt-get update && \
    apt-get install -y libspatialindex-c4v5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m venv venv && \
    venv/bin/pip install -r requirements.txt


CMD ['/app/docker-entrypoint.sh']