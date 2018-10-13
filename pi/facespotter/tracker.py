from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from .arm import Arm
from .facefinder import FaceFinder
import logging
import argparse


class Tracker:
    # angle of view is 62.2 x 48.8
    FOV_X = 62
    FOV_Y = 49

    def __init__(self):
        self.logger = logging.getLogger('facespotter.Tracker')
        self._arm = Arm()
        self._faceFinder = FaceFinder()

    def setup(self):
        self._arm.connect()
        self._faceFinder.load()

    def run(self, loops):
        with PiCamera() as camera:
            time.sleep(0.1)
            raw = PiRGBArray(camera)
            i = 0
            for foo in camera.capture_continuous(raw, format="bgr"):
                imageArray = raw.array
                face = self._faceFinder.find(imageArray)
                if (face is not None):
                    self.__lookAtFace(raw, face)
                raw.flush()
                i += 1
                if (i >= loops):
                    break
                time.sleep(0.5)

    def __lookAtFace(self, imageArray, face):
        fullSize = imageArray.shape()
        imageHeight = fullSize[0]
        imageWidth = fullSize[1]

        targetX = ((face[0] + face[2]/2) / imageWidth - 0.5) * Tracker.FOV_X + Arm.BASE_CENTRE
        targetY = ((face[1] + face[3]/2) / imageHeight - 0.5) * Tracker.FOV_Y + Arm.LIFT_CENTRE

        self._arm.rotate(targetX)
        self._arm.lift(targetY)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("loops", help="Number of loops to run for",
                    type=int)
    args = parser.parse_args()

    tracker = Tracker()
    tracker.setup()
    tracker.run(args.loops)
