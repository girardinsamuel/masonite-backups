"""A InstallCommand Command."""
import os
from cleo import Command
from masonite.utils.helpers import load

from ..BackupJob import BackupJob


package_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class RunBackupCommand(Command):
    """
    Create a backup of your project (by default assets and db)

    backups:run
        {--only-assets=? : Backup only assets}
        {--only-db=? : Backup only database}
        {--dry=? : Make a dry backup to show what is going to be backed-up}
    """

    def __init__(self, app):
        super().__init__()
        self.app = app

    def handle(self):
        only_assets = bool(self.option("only-assets"))
        only_db = bool(self.option("only-db"))
        dry_run = self.option("dry")

        # backup = BackupJob(self.application, config("backups."))
        backup = BackupJob(self.app, {})

        if only_db:
            backup.only_db()
        if only_assets:
            backup.only_assets()

        backup.configure()

        if dry_run:
            backup.summary()
        else:
            backup.run()
