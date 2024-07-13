# Bicycle rent

A backend for a bike rental service that provides a RESTful API to perform the most common basic operations with Redis
license bypassing

# Tech stack

## Docker configuration

- local (can be used in the local development and test section of CI)
- non-local (used in the server part)

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
- Local version JDBC connection string - `jdbc:postgresql://localhost:5432/postgres`. Connect with your favourite DBC. Port from the Docker container - `5432`. You can use DataGrip e.g.

### Valkey (Redis opensource fork)

![valkey test](docs/valkey.png)
This demonstrates a seamless replacement of Redis due to a license change.

- KV for celery
- Cache to reduce database usage
- Local version JDBC connection string - `jdbc:redis://localhost:6379/0`. Connect with your favourite DBC. Port from the Docker container - `6379`. You can use Another Redis Desktop Manager e.g.

