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
        extra_context={"project_name": "nautobot-jobs"},
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


# @pytest.mark.parametrize(
#     "license_info",
#     [
#         ("MIT", "MIT "),
#         (
#             "BSD-3-Clause",
#             "Redistributions of source code must retain the " + "above copyright notice, this",
#         ),
#         ("ISC", "ISC License"),
#         ("Apache-2.0", "Licensed under the Apache License, Version 2.0"),
#         ("GPL-3.0-only", "GNU GENERAL PUBLIC LICENSE"),
#     ],
# )
# def test_bake_selecting_license(cookies, nautobot_jobs_dir, license_info):
#     """Test Bake with license.

#     Args:
#         cookies (_type_): _description_
#         license_info (_type_): _description_
#     """
#     _license, target_string = license_info
#     result = cookies.bake(
#         template=nautobot_jobs_dir,
#         extra_context={"open_source_license": _license},
#     )
#     assert target_string in result.project_path.joinpath("LICENSE").read_text()
#     assert _license in result.project_path.joinpath("pyproject.toml").read_text()


# def test_bake_not_open_source(cookies, nautobot_jobs_dir):
#     """Test Bake with open_source_license=False."""
#     result = cookies.bake(
#         template=nautobot_jobs_dir,
#         extra_context={"open_source_license": "Not open source"},
#     )
#     python_cookie_output = [file_folder.name for file_folder in result.project_path.iterdir()]

#     assert "LICENSE" not in python_cookie_output
#     assert "License" not in result.project_path.joinpath("README.md").read_text()
#     assert "license" not in result.project_path.joinpath("pyproject.toml").read_text()


# @pytest.mark.parametrize(
#     "args",
#     [
#         ({"command_line_interface": "No command-line interface"}, False),
#         ({"command_line_interface": "click"}, True),
#     ],
# )
# def test_bake_with_no_console_script(cookies, args):
#     """Test Bake with no Console Script."""
#     context, is_present = args
#     result = cookies.bake(extra_context=context)
#     # project_path, project_slug, project_dir = project_info(result)
#     project_path, _, project_dir = project_info(result)

#     found_project_files = os.listdir(project_dir)
#     assert ("cli.py" in found_project_files) == is_present

#     pyproject_path = os.path.join(project_path, _DEPENDENCY_FILE)
#     with open(pyproject_path, "r", encoding="utf-8") as pyproject_file:
#         assert ("[tool.poetry.scripts]" in pyproject_file.read()) == is_present


# def test_bake_with_console_script_cli(cookies):
#     """Test Bake with Console Script CLI."""
#     context = {"command_line_interface": "click"}
#     result = cookies.bake(extra_context=context)
#     # project_path, project_slug, project_dir = project_info(result)
#     _, project_slug, project_dir = project_info(result)
#     module_path = os.path.join(project_dir, "cli.py")

#     out = execute([sys.executable, module_path], project_dir)
#     assert project_slug in out

#     out = execute([sys.executable, module_path, "--help"], project_dir)
#     assert "Show this message and exit." in out
