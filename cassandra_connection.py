from cassandra.cluster import Cluster
from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED
from cassandra.auth import PlainTextAuthProvider


class CassandraConnect(object):
    host = '10.204.0.50'
    port = '22'
    username = 'lois'
    password = 'ubuntu-3'


    def connect(self):
        auth_provider = PlainTextAuthProvider(username=self.username, password=self.password)
        cluster = Cluster([self.host], auth_provider=auth_provider, port=self.port)
        session = cluster.connect()
        self.session = session
        # r = session.execute('select * from system_schema.keyspaces')
        # print(r.current_rows)