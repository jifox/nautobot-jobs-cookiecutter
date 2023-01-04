"""Nautobot job to verify hostname matches pattern."""
"""Example Job."""
from nautobot.extras.jobs import Job

class ExampleJob(Job):
    """Job without inputs."""

    class Meta:
        """Meta object boilerplate for intended."""

        name = "Example Job"
        description = "This is an example job."

    def run(self, data, commit):
        """Run method for executing the checks on the devices."""
        # Iterate through each Device object, limited to just the site of NYC.
        pass

jobs = [ExampleJob]