import cv2
import logging
import os

class FaceFinder:

    def __init__(self):
        self.logger = logging.getLogger('facespotter.FaceFinder')

    def load(self, classifierXml="haarcascade_frontalface_default.xml"):
        xmlfile = os.path.join(os.path.dirname(__file__), 'resources/' + classifierXml)
        self.logger.info("Loading classifier XML from:%s", xmlfile)
        self._classifier = cv2.CascadeClassifier(xmlfile)

    def find(self, image):
        cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        foundFaces = self._classifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
                                        flags=cv2.CASCADE_SCALE_IMAGE)

        if (len(foundFaces) == 0):
            self.logger.info("Found no faces")
            return None

        for (x, y, w, h) in foundFaces:
            self.logger.info("Found face at (%d,%d), width: %d, height: %d", x, y, w, h)
            return (x, y, w, h)


