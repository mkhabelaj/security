from psql_observer import DatabaseRelay
from observer.subscriber import Subscriber


class Test(Subscriber):
    def update(self, message):
        print('Test', message)


class TestOne(Subscriber):
    def update(self, message):
        print('TestOne', message)


test = Test()
testO = TestOne()
database_relay = DatabaseRelay('testdb', 'jackson', channel='events')

database_relay.subscribe('database_updates', test)
database_relay.subscribe('database_updates', testO)

database_relay.listen_to_database_changes()
