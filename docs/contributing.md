

# Please keep the docs up to date!



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
