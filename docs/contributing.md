# Contributing to LoNG

## Objectives

It is important to review any contributions with the overall context of what the project is attempting to achieve.

### Reproducablity vs Repeatablity

LoNG should enable researchers to achieve any of the four definitions of reproducibility described in the [Turing Way](https://the-turing-way.netlify.app/reproducible-research/overview/overview-definitions.html#table-of-definitions-for-reproducibility).

![table of definitions for reproducibility](https://the-turing-way.netlify.app/_images/reproducible-matrix.jpg "Table of definitions for reproducibility")

Applying these definitions to LoNG:

- The "managed" functionality should enable the "Reproducible" and "replicable" standards (eg re-using the established analysis methods)
- The "advanced/extended" functionality should enable the "Robust" and "Generalisable" standards (Eg using different analysis methods).


### How reproducible?

The [Software Sustainability Institute](https://www.software.ac.uk) provides some helpful definitions of _how_ reproducible research software should be, depending on the context.

![Levels of reproducibility](https://www.software.ac.uk/sites/default/files/reproducibility-circle.png)

https://www.software.ac.uk/news/new-guide-how-reproducible-should-research-software-be

**LoNG aims to achieve code which is in line with Level-2 ("Research Software as a Tool").
**

- Throughout the project, we will be incorporated code which is _currently_ a mixture of Level-0 ("Barely repeatable") and Level-1 ("Research Software for Publication"). Effort will be required to improve the robustness and generalisation of this code.
- LoNG is too specialised to qualify as Level-3 ("Research Software as Infrastructure").


## Tools required

To build this repo locally,it is assumed that a developer has installed:

- VSCode or a comparable editor
- Docker Desktop or Docker + docker compose
- [`hadolint`](https://hadolint.github.io/hadolint/)


### JupyterLab

Setup a custom jupyter_server_config.py

https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html#prerequisite-a-jupyter-server-configuration-file

```
$ jupyter server --generate-config
```


### NGINX

https://hub.docker.com/_/nginx


To get a "clean" copy fo the config file

(taken from the "Complex configuration" section on this page https://hub.docker.com/_/nginx )

```
$ docker run --name tmp-nginx-container -d nginx
$ docker cp tmp-nginx-container:/etc/nginx/nginx.conf /host/path/nginx.conf
$ docker rm -f tmp-nginx-container
```


## Testing


### CI via GitHub Actions


Debug GH Actions locally using `act` https://github.com/nektos/act
