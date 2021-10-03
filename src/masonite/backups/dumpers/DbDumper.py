
class DbDumper:

    def __init__(self):
        self._database = None
        self._host = "localhost"
        self._port = None
        self._password = None
        self._username = None
        self._options = {}

    def dump(self):
        raise NotImplementedError()

    def set_username(self, username):
        self._username = username
        return self

    def set_password(self, password):
        self._password = password
        return self

    def set_database(self, database):
        self._database = database
        return self

    def set_host(self, host):
        self._host = host
        return self

    def set_port(self, port):
        self._port = port
        return self

    def set_options(self, options):
        self._options = options
        return self
