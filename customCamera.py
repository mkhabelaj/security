from camera.camera import Camera
from observer.subscriber import Subscriber
import json


class CustomCamera(Camera, Subscriber):

    def __init__(self,
                 camera_number,
                 stream_port=0,
                 web_socket_port=0,
                 stream_secret='',
                 initialize_stream=False,
                 *args,
                 **kwargs
                 ):
        super(CustomCamera, self).__init__(
            camera_number,
            initialize_stream=initialize_stream,
            stream_port=stream_port,
            *args,
            **kwargs
        )

        self.web_socket_port = web_socket_port
        self.stream_secret = stream_secret

    def update(self, message):
        message = json.loads(message)
        data = message['data']
        self.show_video = data.get('show_video')
        self.delta_thresh = data.get('delta_thresh')
        self.record_motion = data.get('record_motion')
        self.min_area = data.get('min_area')
        self.email_images = data.get('email_images')
        self.min_email_seconds = data.get('min_email_seconds')
        self.motion_detection = data.get('motion_detection')
        self.display_text_if_occupied = data.get('display_text_if_occupied')
        self.display_text_if_unoccupied = data.get('display_text_if_unoccupied')
        self.resolution_width = data.get('resolution_width')
        self.resolution_height = data.get('resolution_height')
