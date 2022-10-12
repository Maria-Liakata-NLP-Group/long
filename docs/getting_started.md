# Getting Started

This assumes that LoNG has already been [installed](installation.md).


## Create a user



```
htpasswd -c ./nginx/config/htpasswd.admin admin
```

You will be asked to enter your password twice.

<-- Check what happens if you run this command twice -->
<-- Instructions for resetting your password -->
<-- What happens if you start LoNG without a password file? -->

## Launching LoNG

Open your shell and navigate to the directory you installed LoNG in. Then run this command:
```
docker compose up
```

Wait until you should see output from both the `long-webserver-1` and `long-dsnb-1` components:

![Image](./images/docker_compose_up.gif)

(Ignore the URLs given in the output - these are incorrect. See the [relevant bug](https://github.com/Maria-Liakata-NLP-Group/long/issues/24)).

## Launch the browser

With your preferred browser, goto:
```
http://localhost/
```

If everthing has worked correctly then you should see the placeholder landing page, as below:

![Image](./images/placeholder_landing_page.png)
