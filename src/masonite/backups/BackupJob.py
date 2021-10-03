import zipfile
from src.masonite.backups.dumpers.PostgresDumper import PostgresDumper
import pendulum
import tempfile
import shutil
from subprocess import Popen
import os
from os.path import join, isfile, isdir

from masonite.utils.helpers import load


class BackupJob:

    def __init__(self, application, config):
        self.application = application
        # self.config = config
        self.config = {
            "name": "masonite-backups-test",
            "source": {
                "files": [
                    "tests/integrations/templates",
                    "tests/integrations/web.py",
                ],
                "databases": ["mysql", "postgres"],
            },
            "destination": {
                "disks": [
                    "local"
                ]
            }
        }

        self.with_db = True
        self.with_assets = True
        self._filename = ""
        self._db_dumpers = {}
        self._assets = []

    def configure(self):
        self._set_filename()
        self._set_assets()
        self._set_db_dumpers()

    def run(self):
        print(f"Creating backup ... {self._filename}")
        with tempfile.TemporaryDirectory(prefix=self.config.get("name")) as tmp_dir:
            backup_zipfile = join(tmp_dir, self._filename)
            zip_file = zipfile.ZipFile(backup_zipfile, "w")

            # Database backup
            if self.with_db:
                root = "db"
                for connection, dumper in self._db_dumpers.items():
                    print(f"backing up db {connection}:")
                    db_file_name = f"{connection}_db.txt"
                    backup_db_file = join(tmp_dir, db_file_name)
                    dumper.set_options({"-v": ""}).dump(backup_db_file)
                    zip_file.write(backup_db_file, join(root, db_file_name))

            # Assets backup
            if self.with_assets:
                root = "assets"
                for asset in self._assets:
                    zip_file.write(asset, os.path.join(root, asset))

            zip_file.close()

            # TODO: use real destination defined by Masonite disk and storage class to copy zip_file to destination
            storage = self.application.make("storage")
            for disk_name in self.config["destination"]["disks"]:
                storage.disk(disk_name).move(backup_zipfile, self._filename)

        print("Done !")

    def summary(self):
        pass

    def only_db(self):
        self.with_db = True
        self.with_assets = False

    def only_assets(self):
        self.with_assets = True
        self.with_db = False

    def _set_filename(self):
        basename = self.config.get("name")
        self._filename = f"{basename}_{pendulum.now().to_iso8601_string()}.zip"

    def _set_assets(self):
        # list of directories and files
        for file_or_dir in self.config["source"]["files"]:
            if isfile(file_or_dir):
                self._assets.append(file_or_dir)
            elif isdir(file_or_dir):
                for root, dirs, files in os.walk(file_or_dir):
                    for file in files:
                        self._assets.append(join(root, file))
            else:
                print("not handled for now (e.g symlinks)")
        return

    def _set_db_dumpers(self):
        connection_details = load(self.application.make("config.database")).DATABASES
        for connection in self.config["source"]["databases"]:
            connection_env = connection_details[connection]
            if connection == "postgres":
                dumper = PostgresDumper.build(connection_env)
                # TODO: add others
                self._db_dumpers[connection] = dumper
