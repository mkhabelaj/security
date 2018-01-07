import threading

import psycopg2
from psycopg2.extras import RealDictCursor
import os
import sys
import json
import subprocess
from psql_observer import DatabaseRelay
from observer.subscriber import Subscriber
from databaseConfig.databaseTableNotifer import PSQLDatabaseSetup
from customCamera import CustomCamera

DATABASE_NAME = 'cam_config'
TABLE_NAME = 'config'
PASSWORD = 'password'
USER = os.environ['USER']
CHANNEL = 'events'

# get a list of camera positions
camera_positions = CustomCamera.count_system_cameras()

# Create database and config table
subprocess.check_call(['databaseConfig/setup.sh', DATABASE_NAME, PASSWORD])

conn = psycopg2.connect(user=USER, database=DATABASE_NAME, password=PASSWORD)
cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute('select * from {table} LIMIT 1;'.format(table=TABLE_NAME))

# Fetch a dictionary with the database configurations
CAMERA_SETTINGS = cur.fetchone()

databaseChannel = PSQLDatabaseSetup(
    connection=conn,
    database_table=TABLE_NAME,
    channel=CHANNEL
)

# Setup notification event on the table
databaseChannel.create_notify_event()


class Test(Subscriber):
    def update(self, message):
        print('Test', message)


test = Test()
customCam = CustomCamera(0, **CAMERA_SETTINGS)

database_relay = DatabaseRelay(DATABASE_NAME, USER, channel=CHANNEL)

database_relay.subscribe('database_updates', test)
database_relay.subscribe('database_updates', customCam)

# Listen to database changes on a separate thread
thread = threading.Thread(target=database_relay.listen_to_database_changes, args=())
# dies when main thread dies
thread.daemon = True
thread.start()

customCam.initialise_camera()



