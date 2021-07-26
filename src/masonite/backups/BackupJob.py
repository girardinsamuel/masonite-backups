import pendulum


class BackupJob:

    def __init__(self, application, config):
        self.application = application
        self.config = config
        self.with_db = True
        self.with_assets = True

    def configure(self):
        self._set_filename()
        self._set_assets()

    def run(self):
        if self.with_db:
            print("backup db")

        if self.with_assets:
            print("backup assets")

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
        return f"{basename}_{pendulum.now().to_iso8601_string()}.zip"

    def _set_assets(self):
        return
