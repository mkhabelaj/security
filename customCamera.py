from camera.camera import Camera
from observer.subscriber import Subscriber


class CustomCamera(Camera, Subscriber):

    def __init__(self, camera_number, display_on_web=False, *args, **kwargs):
        super(CustomCamera, self).__init__(
            camera_number,
            display_on_web,
            *args,
            **kwargs
        )

    def update(self, message):
        print(message)
        self.motion_detection = True