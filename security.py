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
from randgen.portgen.generator import PortGenerator
from randgen.stringgen.generator import StringGenerator
import time

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

# initialize database observer
database_relay = DatabaseRelay(DATABASE_NAME, USER, channel=CHANNEL)

# initialize generators
string_generator = StringGenerator()
port_generator = PortGenerator(number_of_ports=2)

# list of camera objects
camera_objects = []

for n in camera_positions:
    stream_secret = string_generator.produce_strings()
    ports = port_generator.produce_ports()
    cur.execute("INSERT INTO port_map VALUES ({camera_number},{socket_server_port},{web_socket_server_port},'{stream_secret}');".format(
        camera_number=n,
        socket_server_port=ports[0],
        web_socket_server_port=ports[1],
        stream_secret=stream_secret
    ))
    conn.commit()
    # create camera object for each camera
    camera = CustomCamera(
        camera_number=n,
        stream_port=ports[0],
        web_socket_port=ports[1],
        stream_secret=stream_secret,
        **CAMERA_SETTINGS
    )
    camera_objects.append(camera)
    # subscribe each camera to database events
    database_relay.subscribe('database_updates', camera)
    # set up web socket server

# Listen to database changes on a separate thread
thread = threading.Thread(target=database_relay.listen_to_database_changes, args=())
# dies when main thread dies
thread.daemon = True
thread.start()

main_cam = camera_objects.pop(0)

# initiate all cameras
for cam in camera_objects:
    thread_cam = threading.Thread(target=cam.initialise_camera, args=())
    thread_cam.setDaemon(True)
    thread_cam.start()
    time.sleep(10)

main_cam.initialise_camera()




