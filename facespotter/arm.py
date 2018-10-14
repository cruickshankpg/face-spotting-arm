import serial
import logging

class Arm:

    BASE_CENTRE = 90
    REACH_CENTRE = 45
    LIFT_CENTRE = 100

    def __init__(self, port='/dev/ttyACM0', baud=9600):
        self.port = port
        self.baud = baud
        self.logger = logging.getLogger('facespotter.Arm')

    def connect(self):
        self.logger.info('Connecting to arm using serial: %s and BAUD: %d', self.port, self.baud)
        self._serial = serial.Serial(self.port, self.baud)
        self.logger.debug('Connected to %s', self._serial)
        self.__resetPositions()

    def disconnect(self):
        self.logger.info('Closing serial connection')
        self._serial.close()

    def __send(self, command):
        self.logger.debug('Sending command %s', command)
        self._serial.write(bytes(command, 'utf8'))

    def rotate(self, angle):
        self.logger.info('Rotating to %d degrees', angle)
        command = "b{}".format(angle)
        self.__send(command)
        self._baseAngle = angle

    def reach(self, angle):
        self.logger.info('Reaching to %d degrees', angle)
        command = "r{}".format(angle)
        self.__send(command)
        self._reachAngle = angle

    def lift(self, angle):
        self.logger.info('Lifting to %d degrees', angle)
        command = "l{}".format(angle)
        self.__send(command)
        self._liftAngle = angle

    def open(self):
        self.logger.info('Opening grip')
        self.__send('g0')
        self._gripOpen = True

    def close(self):
        self.logger.info('Closing grip')
        self.__send('g1')
        self._gripOpen = False

    def __resetPositions(self):
        self._baseAngle = Arm.BASE_CENTRE
        self._reachAngle = Arm.REACH_CENTRE
        self._liftAngle = Arm.LIFT_CENTRE
        self._gripOpen = True


