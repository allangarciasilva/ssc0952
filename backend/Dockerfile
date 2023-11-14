# Base build image
FROM python:3.11 AS build

# Installing Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Installing dependencies
WORKDIR /app/
COPY poetry.lock pyproject.toml ./
RUN poetry install

# Compiling protobuf files
COPY ./proto ./proto
RUN poetry run python -m grpc.tools.protoc -I. ./proto/*.proto --python_out=. --pyi_out=.

# Setting up execution files
COPY ./src ./src
CMD ["poetry", "run", "python", "-m", "src.main"]