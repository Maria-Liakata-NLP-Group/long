# Getting Started

This assumes that LoNG has already been [installed](installation.md).


## Launching LoNG

Open your shell and navigate to the directory you installed LoNG in. Then run this command:
```
docker compose up
```

Wait until you should see output from both the `long-webserver-1` and `long-dsnb-1` components:

![Image](./images/docker_compose_up.gif)

(Ignore the URLs given in the output - these are incorrect. See the [relevant bug](https://github.com/Maria-Liakata-NLP-Group/long/issues/24)).

## Launch the browser

With your prefered browser, goto:
```
http://localhost/
```

If anything has worked correctly then you should see the placeholder landing page, as below:

![Image](./images/placeholder_landing_page.png)
