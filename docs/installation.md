
# Installation

## Supported Configurations

At present LoNG is only supported as a standalone tool to be used on a researcher's personal computer. There are two possible ways to install and operate it.

- Installed as a standalone python package, which can be run as a local webapp or as imported into a Jupyter notebook.
- Installed as a collection of docker containers (wrapped up by docker-compose), which includes a webapp and an embedded Jupyter notebook server

In future, it may be supported when installed as a shared tool for a research team. However at present neither the security nor the stability of this configuration has been tested.

## Pre-requisites

The following software must be installed, prior to installing LoNG:

* A Git client. The instructions below assumes the default command line [git client](https://git-scm.com/downloads).
* A python 3.10 instance (either as a virtualenv or a Conda environment).
* Google Chrome. (Other browsers are untested. There is a known problem using Firefox)
* (For the docker installation only) [Docker Desktop](https://docs.docker.com/engine/install/). Both The Docker engine and Docker Compose are required - both of these tools are included in Docker Desktop.

LoNG _should_ work on any common operating system (Windows, MacOS and Linux), though this has not yet been fully tested. [Feedback is welcome](https://github.com/Maria-Liakata-NLP-Group/long/issues/new).


## Installation

At present installation is only possible from the source code. There are no binary packages available.

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

-- END --
