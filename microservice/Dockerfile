FROM python:3.11

WORKDIR /app
RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install

COPY ./proto/ ./proto
RUN touch ./proto/__init__.py && \
    poetry run python -m grpc.tools.protoc ./proto/*.proto -I. --python_out=. --pyi_out=. 2> /dev/null

COPY ./src ./src