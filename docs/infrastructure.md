# Infrastructure

## Docker
[Docker Compose](https://docs.docker.com/compose/) is employed to run a multi-container Docker application.
The file `docker-compose.yml` is employed to configure Docker Compose.
In summary, this Docker Compose file creates:
- a Jupyter notebook server (`dsnb`) running on a `jupyter/datascience-notebook` image,
- a web application (`webapp`) built from the source code in the `src/` directory,
- and a web server (`webserver`) running on an `nginx` image.
These three services are connected to a common `internal` network, which allows them to communicate with each other.

The `webapp` service builds a Docker image using the `Dockerfile` located in the `src/` directory.

## Nginx
[Nginx](https://www.nginx.com/) is employed to distribute incoming traffic (reverse proxy) to the multi-container Docker application.
It acts as an entry point for all incoming requests and routes each request to the appropriate container based on the request's URL.
The Nginx configuration is specified through the `nginx.conf` file.
