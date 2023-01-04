"""Test Bake Nautobot Jobs Cookie."""
import datetime

import pytest

NAUTOBOT_JOBS_COOKIE_OUTPUT = [
    "LICENSE",
    "pyproject.toml",
    "docs",
    "README.md",
    ".gitignore",
    ".github",
    "FAQ.md",
    "tasks.py",
    "invoke.example.yml",
    ".yamllint.yml",
    "development",
    "jobs",
    "GETTING_STARTED.md",
    ".bandit.yml",
    ".flake8",
    ".dockerignore",
]


def test_bake_project(cookies, nautobot_jobs_dir):
    """Test Bake Project."""
    result = cookies.bake(
        template=nautobot_jobs_dir,
        extra_context={"project_name": "nautobot_jobs"},
    )
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "nautobot-jobs"
    assert result.project_path.is_dir()


def test_year_compute_in_license_file(cookies, nautobot_jobs_dir):
    """Test year compute in license file."""
    result = cookies.bake(template=nautobot_jobs_dir)
    license_file_path = result.project_path.joinpath("LICENSE")
    now = datetime.datetime.now()
    assert str(now.year) in license_file_path.read_text()


def test_cookie_output_dir(cookies, nautobot_jobs_dir):
    """Test cookie output dir."""
    result = cookies.bake(template=nautobot_jobs_dir)
    assert set(NAUTOBOT_JOBS_COOKIE_OUTPUT) == set(dirf.name for dirf in result.project_path.iterdir())


@pytest.mark.parametrize(
    "license_info",
    [
        ("Apache-2.0", "Licensed under the Apache License, Version 2.0"),
    ],
)
def test_bake_selecting_license(cookies, nautobot_jobs_dir, license_info):
    """Test Bake with license.

    Args:
        cookies (_type_): _description_
        license_info (_type_): _description_
    """
    _license, target_string = license_info
    result = cookies.bake(
        template=nautobot_jobs_dir,
        extra_context={"open_source_license": _license},
    )
    assert target_string in result.project_path.joinpath("LICENSE").read_text()
    assert _license in result.project_path.joinpath("pyproject.toml").read_text()


def test_bake_not_open_source(cookies, nautobot_jobs_dir):
    """Test Bake with open_source_license=False."""
    result = cookies.bake(
        template=nautobot_jobs_dir,
        extra_context={"open_source_license": "Not open source"},
    )
    python_cookie_output = [file_folder.name for file_folder in result.project_path.iterdir()]

    assert "LICENSE" not in python_cookie_output
    assert "License" not in result.project_path.joinpath("README.md").read_text()
    assert "license" not in result.project_path.joinpath("pyproject.toml").read_text()
