##########################################################################################

# Python container for outputting python requirements
FROM python:3.13-slim AS python-requirements

RUN pip install --upgrade pip

# Export requirements.txt using poetry.
COPY pyproject.toml ./
COPY poetry.lock ./
RUN pip install poetry
RUN pip install poetry-plugin-export
RUN poetry export -f requirements.txt --output /requirements.txt

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
# 3. Set DJANGO_SETTINGS_MODULE to the dev settings module so dev settings are used 
#    for building the image.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DJANGO_SETTINGS_MODULE=app.settings.dev

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Make sure all packages are up to date
RUN apt-get upgrade -y

RUN pip install --upgrade pip

# Copy the requirements.txt file from the previous stage.
COPY --from=python-requirements /requirements.txt /

# Install the project requirements.
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail ./app /app

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
RUN python manage.py collectstatic --noinput --clear
RUN chown -R wagtail:wagtail /app/static

# Run server
CMD ["gunicorn", "app.wsgi:application"]
