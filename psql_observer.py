from observer import observer
import select
import psycopg2


class DatabaseRelay(observer):

    def __init__(self, database_name, database_user, channel, events=['database_updates']):
        self.events = events
        self.channel = channel
        super(DatabaseRelay, self).__init__(events)
        self.conn = psycopg2.connect(user=database_user, database=database_name)

    def listen_to_database_changes(self):
        self.conn.autocommit = True
        cur = self.conn.cursor()
        cur.execute('Listen {channel};'.format(channel=self.channel))

        while True:
            if select.select([self.conn], [], []) != ([], [], []):
                self.conn.poll()
                while self.conn.notifies:
                    notify = self.conn.notifies.pop(0)
                    print(notify.payload)
                    for event in self.events:
                        self.dispatch(self, event, notify.payload)



