import cv2
import logging

class FaceFinder:

    def __init__(self):
        self.logger = logging.getLogger('facespotter.FaceFinder')

    def load(self, classifierXml="haarcascade_frontalface_default.xml"):
        self._classifier = cv2.CascadeClassifier("resources\/{}".format(classifierXml))

    def find(self, image):
        cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        foundFaces = self._classifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
                                        flags=cv2.CASCADE_SCALE_IMAGE)

        if (len(foundFaces) == 0):
            self.logger.info("Found no faces")
            return None

        for (x, y, w, h) in foundFaces:
            self.logger.info("Found face at ({},{}), width: {}, height: {}", x, y, w, h)
            return (x, y, w, h)


