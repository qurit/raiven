from datetime import datetime

from ldap3 import Server, Connection, Reader, ObjectDef

from api import config


class LDAPManager:

    def __init__(self):
        self.server = Server(config.LDAP_HOST, config.LDAP_PORT)
        self.user_base = config.LDAP_USERNAME_BASE
        self.base_dn = config.LDAP_BASE_DN

        if config.AUTH_ENABLED:
            assert Connection(self.server, auto_bind=True)

    def authenticate(self, username, password):
        if not password:
            return None

        cn = self.user_base + username
        connection = Connection(self.server, cn, password)

        if connection.bind():
            return self.add_user(connection, username)
        else:
            return None

    def add_user(self, connection: Connection, username: str):
        search_filter = '(&(objectCategory=person)(objectClass=user)(sAMAccountName=%s))'
        connection.search(self.base_dn, (search_filter % username))

        user_dn = connection.response[0]['dn']
        user_obj = ObjectDef('user', connection)

        reader = Reader(connection, user_obj, user_dn)
        reader.search()

        result = reader.entries[0]

        return {
            'username': username,
            'name': str(result.name),
            'title': str(result.title),
            'department': str(result.department),
            'company': str(result.company),
            'last_seen': str(datetime.now()),
        }
