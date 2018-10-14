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
    RES_X = 640
    RES_Y = 480

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
            camera.resolution = (Tracker.RES_X, Tracker.RES_Y)
            with PiRGBArray(camera) as raw:
                i = 0
                for foo in camera.capture_continuous(raw, format="bgr"):
                    imageArray = raw.array
                    face = self._faceFinder.find(imageArray)
                    if (face is not None):
                        self.__lookAtFace(raw, face)
                    raw.truncate(0)
                    i += 1
                    if (i >= loops):
                        break
                    time.sleep(0.2)

    def __lookAtFace(self, imageArray, face):
        targetX = Arm.BASE_MAX - ((face[0] + face[2]/2) / Tracker.RES_X) * Arm.BASE_RANGE
        targetY = Arm.LIFT_MAX - ((face[1] + face[3]/2) / Tracker.RES_Y) * Arm.LIFT_RANGE

        self._arm.rotate(targetX)
        self._arm.lift(targetY)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("loops", help="Number of loops to run for",
                    type=int)
    args = parser.parse_args()
    logger = logging.getLogger('facespotter')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('facespotter.log')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    tracker = Tracker()
    tracker.setup()
    tracker.run(args.loops)
