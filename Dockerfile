ARG PYTHON_VER=3.8

ARG DOCKER_DEFAULT_PLATFORM=linux/amd64

FROM python:${PYTHON_VER} AS base

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN pip install -U pip  && \
    curl -sSL https://install.python-poetry.org  | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev

FROM base AS test

RUN poetry install --no-interaction --no-root

COPY . .

RUN echo 'Running Black' && \
    black --check --diff . && \
    echo 'Running Yamllint' && \
    yamllint . && \
    echo 'Running pydocstyle' && \
    pydocstyle .

ENTRYPOINT ["pytest"]

CMD ["--color=yes", "--disable-pytest-warnings"]
