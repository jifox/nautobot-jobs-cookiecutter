"""Conftest for Pytests."""
import pathlib

import pytest
from cookiecutter.main import cookiecutter

COOKIECUTTER_PROJECT = str(pathlib.Path(__file__).parent.parent)


@pytest.fixture
def nautobot_jobs_dir():
    """Return the path to the Nautobot Jobs Cookie directory."""
    return f"{COOKIECUTTER_PROJECT}/jobs"


def generate(directory, context):
    """Generate a project."""
    cookiecutter(
        template=COOKIECUTTER_PROJECT,
        output_dir=str(directory),
        no_input=True,
        extra_context=context,
    )
