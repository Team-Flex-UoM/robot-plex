import plex.line_follow as line_follow
import plex.camera as camera
from plex.camera import Camera

cam = Camera()
# initializations
line_follow.init(cam)
while True:
    line_follow.process_roi()