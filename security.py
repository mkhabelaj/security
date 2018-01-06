import psycopg2

from psql_observer import DatabaseRelay
from observer.subscriber import Subscriber
from databaseConfig.setup import PSQLDatabaseSetup

conn = psycopg2.connect(user='jackson', database='testdb', password='password')
print(conn)
tOne = PSQLDatabaseSetup(conn, 'products', 'events', drop_if_exists=True)

tOne.create_notify_event();
# class Test(Subscriber):
#     def update(self, message):
#         print('Test', message)
#
#
# class TestOne(Subscriber):
#     def update(self, message):
#         print('TestOne', message)
#
#
# test = Test()
# testO = TestOne()
# database_relay = DatabaseRelay('testdb', 'jackson', channel='events')
#
# database_relay.subscribe('database_updates', test)
# database_relay.subscribe('database_updates', testO)
#
# database_relay.listen_to_database_changes()

