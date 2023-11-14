# Base build image
FROM python:3.11 AS build

# Installing Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Exporting Poetry dependencies as requirements.txt
WORKDIR /app/
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Base release image
FROM python:3.11 AS release

# Setting up virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Installing dependencies
WORKDIR /app/
COPY --from=build /app/requirements.txt ./
RUN pip install -r requirements.txt

# Copying remaining files to app root
COPY . ./
