# Decide On Development Environment

- [Decide On Development Environment](#decide-on-development-environment)
  - [Introduction](#introduction)
  - [Poetry](#poetry)
  - [Full Docker Development Environment](#full-docker-development-environment)
    - [Invoke (Manual) - Creating a Superuser](#invoke-manual---creating-a-superuser)
    - [Invoke (Manual) - Stopping the Development Environment](#invoke-manual---stopping-the-development-environment)
    - [Real-Time Updates? How Cool](#real-time-updates-how-cool)
  - [Docker Magic](#docker-magic)
    - [Docker Logs](#docker-logs)
  - [To Rebuild or Not to Rebuild](#to-rebuild-or-not-to-rebuild)
    - [Updating Environment Variables](#updating-environment-variables)
    - [Installing Additional Python Packages](#installing-additional-python-packages)
    - [Installing Additional Nautobot Plugins](#installing-additional-nautobot-plugins)
    - [Updating Python Version](#updating-python-version)
    - [Updating Nautobot Version](#updating-nautobot-version)
  - [Local Development Environment](#local-development-environment)
  - [Other Miscellaneous Commands To Know](#other-miscellaneous-commands-to-know)
    - [Python Shell](#python-shell)
    - [Tests](#tests)

## Introduction

The cookie provides the ability to develop and manage the Nautobot server locally (with supporting services being _Dockerized_) or using only Docker containers to manage Nautobot. The main difference between the two environments is the ability to debug and use **pdb** when developing locally. Debugging with **pdb** within the Docker container is more complicated, but can still be accomplished by either exec'ing into the container or attaching your IDE to the container and running the Nautobot service manually within the container.

The upside to having the Nautobot service handled by Docker rather than locally is that you do not have to manage the Nautobot server and the [Docker logs](#docker-logs) provide the majority information you will need to help troubleshoot while getting started quickly and not requiring you to perform several manual steps to get started and remember to have the Nautobot server running or having it run in a separate terminal while you develop. Ultimately, the decision is yours as to how you want to develop, but it was agreed it would be a good idea to provide pros and cons for each development environment.

> The local environment still uses Docker containers for the supporting services (Postgres, Redis, and Celery), but the Nautobot server is handled locally by you, the developer.

Follow the directions below for the specific development environment that you choose.

## Poetry

Poetry is used in lieu of the "virtualenv" commands and is used for either environment. The virtual environment will provide most of the Python packages required to manage the development environment such as **Invoke**, but see the [Local Development Environment](#local-development-environment) section to see how to install Nautobot if you're going to be developing locally. To get started, run the following commands:

```bash
➜ poetry install
➜ poetry shell
```

The first command creates the virtual environment through Poetry and installs all relevant dependencies, as outlined in the `pyproject.toml` file.

The second command puts your shell session into the virtual environment, so all commands ran going forward are from within the virtual environment. (This is similar to running the `source venv/bin/activate` command with virtualenvs).

## Full Docker Development Environment

**Invoke**

The beauty of **Invoke** is that the Cookiecutter template provides several simple CLI commands to get developing fast. You'll use a few `invoke` commands to get your environment up and running.

### Invoke (Manual) - Creating a Superuser

The Nautobot development image will automatically provision a super user when specifying the following variables within `creds.env` which is the default when copying `creds.example.env` to `creds.env`.

- **NAUTOBOT_CREATE_SUPERUSER=true**
- **NAUTOBOT_SUPERUSER_API_TOKEN=0123456789abcdef0123456789abcdef01234567**
- **NAUTOBOT_SUPERUSER_PASSWORD=admin**

> NOTE: The default username is **admin**, but can be overridden by specifying **NAUTOBOT_SUPERUSER_USERNAME**.

If you need to create additional superusers, run the follow commands.

```bash
➜ invoke createsuperuser
Running docker-compose command "ps --services --filter status=running"
Running docker-compose command "exec nautobot nautobot-server createsuperuser --username admin"
Error: That username is already taken.
Username: ntc
Email address: ntc@networktocode.com
Password:
Password (again):
Superuser created successfully.
```

### Invoke (Manual) - Stopping the Development Environment

The last command to know for now is `invoke stop`.

```bash
➜ invoke stop
Stopping Nautobot...
Running docker-compose command "down"
Stopping {{ cookiecutter.project_name }}_worker_1   ...
Stopping {{ cookiecutter.project_name }}_nautobot_1 ...
Stopping {{ cookiecutter.project_name }}_docs_1     ...
Stopping {{ cookiecutter.project_name }}_redis_1    ...
Stopping {{ cookiecutter.project_name }}_postgres_1 ...
Stopping {{ cookiecutter.project_name }}_worker_1   ... done
Stopping {{ cookiecutter.project_name }}_nautobot_1 ... done
Stopping {{ cookiecutter.project_name }}_postgres_1 ... done
Stopping {{ cookiecutter.project_name }}_redis_1    ... done
Stopping {{ cookiecutter.project_name }}_docs_1     ... done
Removing {{ cookiecutter.project_name }}_worker_1   ...
Removing {{ cookiecutter.project_name }}_nautobot_1 ...
Removing {{ cookiecutter.project_name }}_docs_1     ...
Removing {{ cookiecutter.project_name }}_redis_1    ...
Removing {{ cookiecutter.project_name }}_postgres_1 ...
Removing {{ cookiecutter.project_name }}_postgres_1 ... done
Removing {{ cookiecutter.project_name }}_docs_1     ... done
Removing {{ cookiecutter.project_name }}_worker_1   ... done
Removing {{ cookiecutter.project_name }}_redis_1    ... done
Removing {{ cookiecutter.project_name }}_nautobot_1 ... done
Removing network {{ cookiecutter.project_name }}_default
```

This will safely shut down all of your running Docker containers for this project. When you are ready to spin containers back up, it is as simple as running `invoke start` again like in [**Invoke - Starting the Development Environment**](#invoke---starting-the-development-environment).

> NOTE: If you're wanting to reset the database and configuration settings, you can use the `invoke destroy` command, but it will result in data loss so make sure that is what you want to do.

### Real-Time Updates? How Cool

Your environment should now be fully setup, all necessary Docker containers are created and running, and you're logged into Nautobot in your web browser. Now what?

Now you can start developing your jobs in the folder generated for you by Cookiecutter.

## Docker Magic

The magic here is the root directory is mounted inside your Docker containers when built and ran, so **any** changes made to the files in here are directly updated to the Nautobot jobs code running in Docker.

> NOTE: There are a few exceptions to this, as outlined in the section [To Rebuild or Not To Rebuild](#to-rebuild-or-not-to-rebuild).

> NOTE: You may get connection refused while Django reloads, but it should be refreshed fairly quickly.

### Docker Logs

When trying to debug an issue, one helpful thing you can look at are the logs within the Docker containers.

```bash
➜ docker logs <name of container> -f
```

> NOTE: The `-f` tag will keep the logs open, and output them in realtime as they are generated.

So for example, our plugin is named `{{ cookiecutter.project_slug }}`, the command would most likely be `docker logs {{ cookiecutter.project_name }}_nautobot_1 -f`. You can find the name of all running containers via `docker ps`.

If you want to view the logs specific to the worker container, simply use the name of that container instead.

## To Rebuild or Not to Rebuild

Most of the time, you will not need to rebuild your images. Simply running `invoke start` and `invoke stop` is enough to keep your environment going.

However there are a couple of instances when you will want to.

### Updating Environment Variables

To add environment variables to your containers, thus allowing Nautobot to use them, you will update/add them in the `development/dev.env` file. However, doing so is considered updating the underlying container shell, instead of Django (which auto restarts itself on changes).

To get new environment variables to take effect, you will need stop any running images, rebuild the images, then restart them. This can easily be done with 3 commands:

```bash
➜ invoke stop
➜ invoke build
➜ invoke start
```

Once completed, the new/updated environment variables should now be live.

### Installing Additional Python Packages

If you want your plugin to leverage another available Nautobot plugin or another Python package, you can easily add them into your Docker environment.

```bash
➜ poetry shell
➜ poetry add netutils
```

Once the dependencies are resolved, stop the existing containers, rebuild the Docker image, and then start all containers again.

```bash
➜ invoke stop
➜ invoke build
➜ invoke start
```

### Installing Additional Nautobot Plugins

Let's say for example you want the new plugin you're creating to integrate into Slack. To do this, you will want to integrate into the existing Nautobot ChatOps Plugin.

```bash
➜ poetry shell
➜ poetry add nautobot-chatops-plugin
```

Once you activate the virtual environment via Poetry, you then tell Poetry to install the new plugin.

Before you continue, you'll need to update the file `development/nautobot_config.py` accordingly with the name of the new plugin under `PLUGINS` and any relevant settings as necessary for the plugin under `PLUGINS_CONFIG`. Since you're modifying the underlying OS (not just Django files), you need to rebuild the image. This is a similar process to updating environment variables, which was explained earlier.

```bash
➜ invoke stop
➜ invoke build
➜ invoke start
```

Once the containers are up and running, you should now see the new plugin installed in your Nautobot instance.

You can even launch an `ngrok` service locally on your laptop, pointing to port 8080 (such as for chatops development), and it will point traffic directly to your Docker images. How cool!

### Updating Python Version

To update the Python version, you can update it within `tasks.py`.

```python
namespace = Collection("{{ cookiecutter.project_name }}")
namespace.configure(
    {
        "{{ cookiecutter.project_name }}": {
            ...
            "python_ver": "3.7",
	    ...
        }
    }
)
```

Or set the `INVOKE_{{ cookiecutter.project_name.upper() }}_PYTHON_VER` variable

### Updating Nautobot Version

To update the Python version, you can update it within `tasks.py`.

```python
namespace = Collection("{{ cookiecutter.project_name }}")
namespace.configure(
    {
        "{{ cookiecutter.project_name }}": {
            ...
            "nautobot_ver": "1.0.2",
	    ...
        }
    }
)
```

Or set the `INVOKE_{{ cookiecutter.project_name.upper() }}_NAUTOBOT_VER` variable

## Local Development Environment

Refer back to the [README](./README.md) for developing locally.

## Other Miscellaneous Commands To Know

### Python Shell

To drop into a Django shell for Nautobot (in the Docker container) run:

```bash
➜ invoke nbshell
```

This is the same as running:

```bash
➜ invoke cli
➜ nautobot-server nbshell
```

### Tests

To run tests against your code, you can run all of the tests that in CI runs against any new PR with:

```bash
➜ invoke tests
```

To run an individual test, you can run any or all of the following:

```bash
➜ invoke unittest
➜ invoke bandit
➜ invoke black
➜ invoke flake8
➜ invoke pydocstyle
➜ invoke pylint
```

[Home](README.md)
