"""Plugin declaration for {{ cookiecutter.project_name }}."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)


from nautobot.core.signals import nautobot_database_ready
from nautobot.apps import NautobotAppConfig

from {{ cookiecutter.project_name }}.signals import nautobot_database_ready_callback


class {{ cookiecutter.camel_name }}PluginConfig(PluginConfig):
    """Plugin configuration for the nautobot_ssot plugin."""

    name = "{{ cookiecutter.project_name }}"
    verbose_name = "{{ cookiecutter.verbose_name }}"
    version = __version__
    author = "{{ cookiecutter.full_name }}"
    description = "{{ cookiecutter.project_short_description }}"
    base_url = "{{ cookiecutter.app_base_url }}"
    required_settings = []
    min_version = "{{ cookiecutter.min_nautobot_version }}"
    max_version = "{{ cookiecutter.max_nautobot_version }}"
    default_settings = {
        "hide_example_jobs": False,
    }
    caching_config = {}

    # # URL reverse lookup names
    # home_view_name = "plugins:{{ cookiecutter.project_name }}:home"
    # config_view_name = "plugins:{{ cookiecutter.project_name }}:config"
    # docs_view_name = "plugins:{{ cookiecutter.project_name }}:docs"

    def ready(self):
        """Callback when this app is loaded."""
        super().ready()
        # Connect the nautobot_database_ready_callback() function to the nautobot_database_ready signal.
        # This is by no means a requirement for all plugins, but is a useful way for a plugin to perform
        # database operations such as defining CustomFields, Relationships, etc. at the appropriate time.
        nautobot_database_ready.connect(nautobot_database_ready_callback, sender=self)


config = {{ cookiecutter.camel_name }}PluginConfig  # pylint:disable=invalid-name
