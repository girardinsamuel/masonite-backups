"""A BackupsProvider Service Provider."""

from masonite.providers import Provider
from ..commands.RunBackupCommand import RunBackupCommand


class BackupsProvider(Provider):
    """Provides Services To The Service Container."""

    def __init__(self, app):
        self.application = app

    def register(self):
        """Register objects into the Service Container."""
        self.application.make("commands").add(RunBackupCommand(self.application))
        pass

    def boot(self):
        """Boots services required by the container."""
        pass
