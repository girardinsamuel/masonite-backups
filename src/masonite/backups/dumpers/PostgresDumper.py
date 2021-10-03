from subprocess import Popen
import platform

from .DbDumper import DbDumper


class PostgresDumper(DbDumper):

    def __init__(self):
        super().__init__()
        self._port = 5432

    def dump(self, filename):
        env = self.get_env()
        flags = self.get_options_flags()
        try:
            if platform.system() != 'Windows':
                print(f'pg_dump -f {filename} -F tar -w {flags}')
                print(env)
                process = Popen([f'pg_dump -f {filename} -F tar -w {flags}'],
                                shell=True,
                                env=env
                            )
                process.wait()
            else:
                print(['pg_dump', '-f', filename, '-F', 'tar', '-w'] + flags.split(" "))
                process = Popen(['pg_dump', '-f', filename, '-F', 'tar', '-w'] + flags.split(" "),
                                shell=True,
                                env=env
                            )
                process.wait()
        except Exception as e:
            raise Exception("Backup PostgreSQL FAIL!", e)

    @classmethod
    def build(cls, options):
        return (cls()
            .set_database(options.get("database"))
            .set_host(options.get("host"))
            .set_username(options.get("user"))
            .set_password(options.get("password"))
            .set_port(options.get("port"))
        )

    def get_env(self):
        return {
            "PGDATABASE": str(self._database),
            "PGPORT": str(self._port),
            "PGUSER": str(self._username),
            "PGHOST": str(self._host),
        }

    def get_options_flags(self):
        flags = ""
        for flag, value in self._options.items():
            flags += f" {flag} {value}"
        return flags
