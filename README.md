# Wagtail App Nest

:construction:***Work in progress***:construction:

A template for starting new Django and Wagtail CMS applications with an integrated frontend. Features include:
- Django/Wagtail setup.
- Flexible Pages app for creating multi-purpose pages.
- Menus app for building menus from the CMS.
- Nest app as a toolbox containing reusable abstract models, mixins, fields, stream field blocks, helper functions, templates, and template tags.
- Custom Wagtail image and document models.
- Custom user model.
- Front-end setup with Vite.js.
- Vue.js and Sass with a simple style framework for quick styling and prototyping.
- Main menu as a Vue.js component (which uses the data from the Menus app).

This repository is set as a GitHub template and can be used to generate a new repository with the same directory structure and files but with fresh and independent Git history. Check [creating a repository from a template on GitHub](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template).

## Setup

You can use Docker Compose to run the entire application stack, including the Django backend and the Vue.js frontend, within isolated containers. This method is ideal for maintaining consistency across different development environments and simplifying the setup process.

**Note:** The default Docker Compose setup uses an **SQLite** database. If you need a PostgreSQL setup, it is available as described in the [PostgreSQL](#postgresql) section below.

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Steps
In the root of the project (where the `docker-compose.yml` file is), follow these steps:

**1. Build the Docker images:**
  ```sh
  docker compose build
  ```

**2. Run the containers:**
  ```sh
  docker compose up
  ```

**3. Access the container interface (for running commands like migrations):**
  ```sh
  docker compose exec app bash
  ```

**4. Run migrations and create a superuser:**
  ```sh
  python manage.py migrate
  python manage.py createsuperuser
  ```

**5. Access the application:**
  - The application will be available at [http://localhost:8000](http://localhost:8000).
  - The frontend assets will be served with hot reload from [http://localhost:5173](http://localhost:5173).
  - The CMS can be accessed at [http://localhost:8000/admin/](http://localhost:8000/admin/) using the credentials of the superuser you created.

### PostgreSQL

To run the application with a PostgreSQL database locally, replace steps 1 and 2 with these:

**1. Build the Docker images:**
  ```sh
  docker compose -f docker-compose.yml -f docker-compose.postgres.yml build
  ```

**2. Run the containers:**
  ```sh
  docker compose -f docker-compose.yml -f docker-compose.postgres.yml up
  ```

This setup configures the application to use PostgreSQL as the database. You can then proceed with the remaining steps as usual.

To run Postgres client commands, use `docker compose exec db <command>`. Examples include:

**Running a Postgres shell:**
```sh
docker compose exec db psql postgres -U postgres
```

**Dumping a database using `pg_dump`:**
```sh
docker compose exec db pg_dump postgres -U postgres > dump.sql
```

**Restoring a previously dumped database:**
```sh
docker compose exec db psql postgres -U postgres < dump.sql
```

## Django Wagtail backend

This is the backend application based on Django and Wagtail CMS, contained within the `/app/` directory.

If you want to install new packages or update current ones, you need to do it outside of the Docker containers by running Python poetry commands and having Python installed on your operating system.

- [Python 3.13](https://www.python.org/downloads/)
- [Python poetry 2.0+](https://python-poetry.org/docs/#installation)

## Frontend

The frontend leverages [Vue.js 3](https://v3.vuejs.org/guide/introduction.html) with a multiple instance approach, utilizing TypeScript and Sass for interactivity and styling within Django templates.

Assets are built and served using [ViteJS](https://vite.dev/) from the `/frontend/` directory. Django integrates these compiled assets through [django-vite](https://github.com/MrBin99/django-vite). Ensure the Vite development server is running concurrently with the Django server for proper functionality.

As for the backend, if you want to install new packages or update current ones, you need to do it outside of the Docker containers by running `npm` commands. You will need [Node 20.18+](https://nodejs.org/en/download) installed on your system.
