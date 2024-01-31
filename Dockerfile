FROM python:3.10.12 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10.12

ENV PYTHONFAULTHANDLER=1 \
        PYTHONUNBUFFERED=1 \
        PYTHONHASHSEED=random \
        PIP_NO_CACHE_DIR=off \
        PIP_DISABLE_PIP_VERSION_CHECK=on \
        PIP_DEFAULT_TIMEOUT=100 \
        PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get -y install libxft-dev libffi-dev libssl-dev && \
    apt-get -y install ncat && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/.