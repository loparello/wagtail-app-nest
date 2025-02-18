##########################################################################################

# Node build container for frontend assets
# Builds from source and prepares assets for collection by multi build step
FROM node:20-slim AS asset-builder

WORKDIR /frontend

# Copy package.json and package-lock.json first to leverage Docker cache
COPY ./frontend/package*.json /frontend/

RUN npm install

COPY ./frontend/vite.config.ts /frontend/
COPY ./frontend/tsconfig*.json /frontend/
COPY ./frontend/eslint.config.js /frontend/
COPY ./frontend/src /frontend/src

# Production build command
RUN npm run build

# Files are available in /frontend/dist - ready to copy out into the django container into: /app/assets

##########################################################################################

# Python container for outputting python requirements
FROM python:3.13-slim AS python-requirements

RUN pip install --upgrade pip

# Export requirements.txt using poetry.
COPY pyproject.toml ./
COPY poetry.lock ./
RUN pip install poetry
RUN pip install poetry-plugin-export
RUN poetry export -f requirements.txt \
 --with pgsql \
 --output /requirements.txt

##########################################################################################

# Use an official Python runtime based on Debian slim as a parent image.
FROM python:3.13-slim

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE" command.
# 3. Set DJANGO_SETTINGS_MODULE to the base settings module so dev settings are not used 
#    for building the image (this is a staging/production image).
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DJANGO_SETTINGS_MODULE=app.settings.base

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Make sure all packages are up to date
RUN apt-get upgrade -y

RUN pip install --upgrade pip

# Copy the requirements.txt file from the previous stage.
COPY --from=python-requirements /requirements.txt /

# Install the project requirements plus gunicorn server and psycopg2 to support PostgreSQL
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail ./app /app

# Copy in our frontend assets from a multi-build step
COPY --from=asset-builder --chown=wagtail /frontend/dist /app/assets

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
RUN python manage.py collectstatic --noinput --clear
RUN chown -R wagtail:wagtail /app/static

# Run server
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
