# Bicycle rent

A backend for a bike rental service that provides a RESTful API to perform the most common basic operations with Redis
license bypassing

## Tech info

## Docker configuration

- local (can be used in the local development and test section of CI)
- non-local (used in the server part)

In the local project configuration, the app folder on your machine is mounted as a volume to the app folder in the
container.
This allows you to make changes to the code and see the updates immediately.
Additionally, you can use the remote Python interpreter from the container in your IDE, ensuring a convenient and
efficient development process.
![interpreter1](docs/interpreter1.png)

Next choose local.docker-compose.yml

![interpreter2](docs/interpreter2.png)

### Python 3.10 on alpine

One image for 4 containers (shared style, build 1 time and up via different commands)

- Django as web framework
- Celery as worker
- Celery Beat as scheduler
- Flower to monitor and control tasks + export to Grafana via API.

### PostgreSQL 13 on alpine

- Container with shared volume
- Default user for Django
- Default config light version
- Local version JDBC connection string - `jdbc:postgresql://localhost:5432/postgres`. Connect with your favourite DBC.
  Port from the Docker container - `5432`. You can use DataGrip e.g.

### Valkey (Redis opensource fork)

![valkey test](docs/valkey.png)
This demonstrates a seamless replacement of Redis due to a license change.

- KV for celery
- Cache to reduce database usage
- Local version JDBC connection string - `jdbc:redis://localhost:6379/0`. Connect with your favourite DBC. Port from the
  Docker container - `6379`. You can use Another Redis Desktop Manager e.g.

### Python dependencies

To manage dependencies in this project, I chose to use pip and a simple requirements.txt file.
There is no need for a private repository such as Nexus, since all dependencies are available in the public PyPI
repositories.
A small list of dependencies allows for efficient use of the simple file, as well as easy installation and updating of
libraries.

- **Django 5.0.7** - High-level Python web framework for rapid development and clean design.
- **Django REST framework 3.15.2** - Powerful and flexible toolkit for building Web APIs.
- **djangorestframework-simplejwt 5.3.1** - JSON Web Token authentication for Django REST framework.
- **celery 5.4.0** - Distributed task queue for real-time processing.
- **flower 2.0.1** - Web-based tool for monitoring and administrating Celery clusters.
- **psycopg2-binary 2.9.9** - PostgreSQL database adapter for Python; binary package, no compilation needed.
- **redis 5.0.7** - In-memory data structure store used as a database, cache, and message broker.
- **black 24.4.2** - Uncompromising Python code formatter ensuring consistent style.
- **flake8 7.1.0** - Tool for enforcing Python style guide and checking code quality. (used in CI job)
- **coverage 7.6.0** - A tool for measuring code coverage of Python programs.

## Testing section

You can manually test application from your docker container before pushing.

### CI:

- Lint test.
- Code test
- Coverage report

```shell
docker exec -it br_app_local sh
```

```shell
coverage run --source='.' manage.py test
```

To see results in your console

```shell
coverage report
```

To generate results in the hidden htmlcov folder

```shell
coverage html
```

To see HTML report at your browser cd to the `/bicycle-rental/app` directory at your system or just open generated HTML
file:

```shell
xdg-open htmlcov/index.html
```

### Test API with Postman

![postman](docs/postman.png)

### Lint test and code quality

Manually in container. This will make code prettier.

```shell
black .
``` 

Then

```shell
flake8 .
```

![postman](docs/lint.png)

Fix all mistakes and continue your important development.   