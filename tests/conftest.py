"""Conftest for Pytests."""
import pathlib

import pytest
from cookiecutter.main import cookiecutter

COOKIECUTTER_COLLECTION = str(pathlib.Path(__file__).parent.parent)


@pytest.fixture
def python_cookie_dir():
    """Return the path to the Python Cookie directory."""
    return f"{COOKIECUTTER_COLLECTION}/python"


@pytest.fixture
def ansible_cookie_dir():
    """Return the path to the Ansible Cookie directory."""
    return f"{COOKIECUTTER_COLLECTION}/ansible"


def generate(directory, context):
    """Generate a project."""
    cookiecutter(
        template=COOKIECUTTER_COLLECTION,
        output_dir=str(directory),
        no_input=True,
        extra_context=context,
    )
