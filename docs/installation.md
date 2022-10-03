
# Installation

## Supported Configurations

At present LoNG is only supported as a standalone tool to be used on a researcher's personal computer.

In future it may be supported when installed as a shared tool for a research team. However at present neither the security nor the stability of this configuration has been tested.

## Pre-requisites

The following software must be installed, prior to installing LoNG:

* [Docker Desktop](https://docs.docker.com/engine/install/). Both The Docker enginee and Docker Compose are required - both of these tools are included in Docker Desktop.
* A Git client. The instructions below assumes the default command line [git client](https://git-scm.com/downloads).

* LoNG _should_ work on any common operating system (Windows, MacOS and Linux), though this has not yet been fully tested. [Feedback is welcome](https://github.com/Maria-Liakata-NLP-Group/long/issues/new).


## Installation

### Clone the repository

* Open an shell
* Create a new directory somewhere suitable in your home/personal drive. The switch to that directory:

```
mkdir /home/jbloggs/work/example/
cd  /home/jbloggs/work/example/
```

* Clone the repo(sitory) using this command:

```
git clone https://github.com/Maria-Liakata-NLP-Group/long.git
```

This will create a directory called `long`. Change directory into this:

```
cd long
```

### Pull the Docker images (optional)

The first time LoNG is run, it will download some Docker images. To force the download (and cache) the images, without starting LoNG, use the following command.

```
docker compose pull .
```

-- END --
