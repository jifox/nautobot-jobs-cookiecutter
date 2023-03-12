"""Nautobot development configuration file."""
import os

from nautobot.core.settings import *  # noqa: F403
from nautobot.core.settings_funcs import is_truthy

#########################
#                       #
#   Required settings   #
#                       #
#########################

# This is a list of valid fully-qualified domain names (FQDNs) for the Nautobot server. Nautobot will not permit write
# access to the server via any other hostnames. The first FQDN in the list will be treated as the preferred name.
#



# Debugging defaults to True rather than False for the development environment
#
DEBUG = is_truthy(os.getenv("NAUTOBOT_DEBUG", "True"))

# Django Debug Toolbar - enabled only when debugging
if DEBUG:
    if "debug_toolbar" not in INSTALLED_APPS:  # noqa: F405
        INSTALLED_APPS.append("debug_toolbar")  # noqa: F405
    if "debug_toolbar.middleware.DebugToolbarMiddleware" not in MIDDLEWARE:  # noqa: F405
        MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
    # By default the toolbar only displays when the request is coming from one of INTERNAL_IPS.
    # For the Docker dev environment, we don't know in advance what that IP may be, so override to skip that check
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _request: DEBUG}

#
# Logging for the development environment, taking into account the redefinition of DEBUG above
#

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOGGING["loggers"]["nautobot"]["handlers"] = ["verbose_console" if DEBUG else "normal_console"]  # noqa: F405
LOGGING["loggers"]["nautobot"]["level"] = LOG_LEVEL  # noqa: F405

#
# Plugins
#

PLUGINS = []

METRICS_ENABLED = True

CELERY_WORKER_PROMETHEUS_PORTS = [8080]


################################################################################
#
#  {{ cookiecutter.project_name }} Plugin-Settings
#
################################################################################

{{ cookiecutter.project_name | upper }}_ENABLED = is_truthy(os.getenv("{{ cookiecutter.project_name | upper }}_ENABLED", False))
if {{ cookiecutter.project_name | upper }}_ENABLED in PLUGINS:

    if "{{ cookiecutter.project_name }}" not in PLUGINS:
        PLUGINS.append("{{ cookiecutter.project_name }}")

    if "{{ cookiecutter.project_name }}" not in PLUGINS_CONFIG:
        LOGGING["loggers"]["{{ cookiecutter.project_name }}"] = {}
        LOGGING["loggers"]["{{ cookiecutter.project_name }}"]["handlers"] = ["verbose_console" if DEBUG else "normal_console"]  # noqa: F405
        LOGGING["loggers"]["{{ cookiecutter.project_name }}"]["level"] = LOG_LEVEL  # noqa: F405

        # Plugins configuration settings. These settings are used by various plugins that the user may have installed.
        # Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
        PLUGINS_CONFIG.update(
            {
                "{{ cookiecutter.project_name }}": {
                },
            }
        )
