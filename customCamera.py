from camera.camera import Camera
from observer.subscriber import Subscriber
import json


class CustomCamera(Camera, Subscriber):

    def __init__(self, camera_number, display_on_web=False, *args, **kwargs):
        super(CustomCamera, self).__init__(
            camera_number,
            display_on_web,
            *args,
            **kwargs
        )

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
