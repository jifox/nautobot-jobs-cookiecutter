# Nautobot Jobs Cookiecutter

> NOTE: This was originally forked from [Nautobot Chatops Cookiecutter](https://github.com/h4ndzdatm0ld/nautobot-jobs-cookiecutter)

This project helps to get you started on developing Nautobot Jobs quickly. When running through the cookie cutter template, there are a few questions that will help dynamically create content within the final "baked cookie" project.

## Jobs Repository

Nautobot has multiple ways in which `Jobs` can be ingested. This cookie will create a scaffold for a new directory layout that will be a `Git Repository` object inside of Nautobot. Additionally, it will give you a development environment to automatically mount the jobs in the correct directory based on the [Jobs Documentation](https://docs.nautobot.com/projects/core/en/stable/additional-features/jobs/)

## Why Cruft & Cookiecutter?

Before we get started, let's provide some context around the terminology used within Cookiecutter. What is this Cookiecutter? It is a Python method of creating new projects/files from a templated base. Cookiecutter is an open source command-line tool to create projects from a project template. You can learn more on the Cookiecutter [GitHub](https://github.com/cookiecutter/cookiecutter) and [ReadTheDocs](https://cookiecutter.readthedocs.io/en/stable/). Cruft is the method in which you should bake your cookie to ensure that you can always stay up to date with the latest changes to this project.

- **cookie** - The Cookiecutter template that provides the framework for specific projects to allow developers to get started developing faster such as the ones defined above.
- **bake/baking** - The output of a cookie. If a cookie is baked, it means the project was created from a Cookiecutter template.

Cookiecutter was chosen as a method to create projects from a template because it provides the capability to provide a customized project output based on a question/answer setup to help get customization in place.

Check out the [Python Cookiecutter documentation](https://cookiecutter.readthedocs.io/en/1.7.2/) and the[Cruft](https://lyz-code.github.io/blue-book/linux/cruft/) for more details of the project.

## Getting Started

Below are the steps outlined in detail for getting started along with various tips and tricks that may be beneficial.

## Generating a New Nautobot Jobs Project

> NOTE: Recommend to use [Cruft](https://lyz-code.github.io/blue-book/linux/cruft/) to bake cookies to keep track of future changes and the ability to keep your cookie up to date.

Let's walk you through baking a **nautobot-jobs** cookie. Below are the settings that will be asked for during the question part.

| Setting | Description |
| --- | --- |
| **full_name** | Used in the **author** field within `pyproject.toml` and `PluginConfig` |
| **email** | Used in the **author** field within `pyproject.toml` |
| **repo_name** | The Python name of the plugin |
| **verbose_name** | Used in `PluginConfig` |
| **plugin_slug** | Python packaging name |
| **project_slug** | Slug for the project |
| **base_url** | Defines plugin's base url used in Nautobot |
| **min_nautobot_version** | The minimum supported Nautobot version |
| **max_nautobot_version** | The maximum supported Nautobot version |
| **nautobot_version** | Used for development purposes to decide with Nautobot-dev Docker image to use for development |
| **camel_name** | Used to define the plugin's subclassing of `PluginConfig`, e.g. `MyPluginConfig(PluginConfig):` |
| **project_short_description** | Used in the **description** field within `PluginConfig` |
| **version** | Version of the new Nautobot plugin |
| **open_source_license** | Determine if project is open source or not |

> NOTE: Cookiecutter by default bakes the new cookie within the current working directory. If that is not desirable then use the `-o` option to specify a different output directory.

```bash
❯ cookiecutter .

full_name [John Doe]: email [mail@example.com]:
repo_name [nautobot_plugin_chatops_my_plugin]:
verbose_name [Nautobot Plugin Chatops My Plugin]:
plugin_slug [nautobot-plugin-chatops-my-plugin]:
project_slug [nautobot-plugin-chatops-my-plugin]:
min_nautobot_version [1.2.0]:
max_nautobot_version [1.9999]:
nautobot_version [latest]:
camel_name [NautobotPluginChatopsMyPlugin]:
project_short_description [Nautobot Plugin Chatops My Plugin]:
version [0.1.0]:
Select open_source_license:
1 - Apache-2.0
2 - Not open source
Choose from 1, 2 [1]:

Congratulations!  Your cookie has now been baked.

⚠️⚠️ Before you start using your cookie you must run the following commands inside your cookie:

* cp development/creds.example.env development/creds.env
* poetry lock

creds.env will be ignored by git and can be used to override default environment variables.
```

Follow the directions provided at the end of baking the cookie.

```bash
➜ cd nautobot-plugin-chatops-my-plugin
➜ poetry lock
➜ cp development/creds.example.env development/creds.env
```

Here is an example of what your directory structure may look like (structure may change over time).

> NOTE: there are hidden files not displayed in the below output.

```bash
➜ ll nautobot-plugin-chatops-my-plugin
total 104
-rw-r--r--  1 ntc  staff    29B Aug  3 08:15 FAQ.md
-rw-r--r--  1 ntc  staff    16K Aug  3 08:15 GETTING_STARTED.md
-rw-r--r--  1 ntc  staff   591B Aug  3 08:15 LICENSE
-rw-r--r--  1 ntc  staff   7.1K Aug  3 08:15 README.md
drwxr-xr-x  9 ntc  staff   288B Aug  3 08:15 development
-rw-r--r--  1 ntc  staff   300B Aug  3 08:15 invoke.example.yml
drwxr-xr-x  7 ntc  staff   224B Aug  3 08:15 nautobot_plugin_chatops_my_plugin
-rw-r--r--  1 ntc  staff   2.3K Aug  3 08:15 pyproject.toml
-rw-r--r--  1 ntc  staff    12K Aug  3 08:15 tasks.py
```

Once the cookie is baked the next step is to start developing the plugin! To get familiar with the development environment provided by this cookie, we recommend checking out the `GETTING_STARTED.md` or `README.md` located in the root directory of the newly baked cookie.

**Nautobot**

- Got to <http://localhost:8080>
- Log in using the default `admin/admin` credentials.
  - These are set in `development/creds.env`, and may have been changed.
