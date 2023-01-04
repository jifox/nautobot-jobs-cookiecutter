#!/usr/bin/env python
"""Post Gen Hooks."""
import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath) -> None:
    """Remove a file."""
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def main() -> None:
    """Main."""
    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")

    print("\nCongratulations!  Your cookie has now been baked.\n")
    print("⚠️⚠️ Before you start using your cookie you must run the following commands inside your cookie:\n")
    print("* cd {{ cookiecutter.project_slug }}")
    print("* cp development/creds.example.env development/creds.env\n* poetry lock\n")
    print("creds.env will be ignored by git and can be used to override default environment variables.\n")


if __name__ == "__main__":
    main()
