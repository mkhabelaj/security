import json
import threading
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import subprocess
from psql_observer import DatabaseRelay
from databaseConfig.databaseTableNotifer import PSQLDatabaseSetup
from customCamera import CustomCamera
from randgen.portgen.generator import PortGenerator
from randgen.stringgen.generator import StringGenerator
import time


def create_value_string(list_item):
    value = []
    for item in list_item:
        if isinstance(item, (int, float)):
            value.append(item)
        else:
            value.append(wrap_with_quotes(item))
    values = ','.join(str(v) for v in value)
    return values


def wrap_with_quotes(x):
    return "'%s'" % x

DATABASE_NAME = 'cam_config'
TABLE_NAME = 'config'
PASSWORD = 'password'
USER = os.environ['USER']
CHANNEL = 'events'

# Get current ip from wifi
f = os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
CURRENT_IP = f.read()
CURRENT_IP = CURRENT_IP[:-1] if CURRENT_IP else 'localhost'

# get a list of camera positions
camera_positions = CustomCamera.count_system_cameras()

# Create database and config table
subprocess.check_call(['databaseConfig/setup.sh', DATABASE_NAME, PASSWORD])

conn = psycopg2.connect(user=USER, database=DATABASE_NAME, password=PASSWORD)
cur = conn.cursor(cursor_factory=RealDictCursor)

# Fetch a dictionary with the database configurations
CAMERA_SETTINGS = json.load(open('databaseConfig/config.json'))

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
    cur.execute(
        "INSERT INTO port_map VALUES "
        "('{stream_secret}',{camera_number},{socket_server_port},{web_socket_server_port},'{ip_address}');".format(
            camera_number=n,
            socket_server_port=ports[0],
            web_socket_server_port=ports[1],
            stream_secret=stream_secret,
            ip_address=CURRENT_IP
        )
    )

    CAMERA_SETTINGS['stream_key'] = stream_secret
    conn.commit()
    key_values = ",".join(CAMERA_SETTINGS.keys())
    cur.execute('insert into config ({keys}) VALUES ({values})'.format(
        values=create_value_string(CAMERA_SETTINGS.values()),
        keys=key_values
    ))
    conn.commit()
    subprocess.check_call(
        ['./initiate_screen.sh', stream_secret, stream_secret, str(ports[0]), 'security', str(ports[1]), stream_secret])
    time.sleep(5)
    # create camera object for each camera
    camera = CustomCamera(
        camera_number=n,
        stream_port=ports[0],
        web_socket_port=ports[1],
        stream_secret=stream_secret,
        initialize_stream=True,
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


main_cam.initialise_camera()