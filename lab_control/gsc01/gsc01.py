import serial
import time


_WAIT_TIME = 0.3  # wait 3 second if not respond


class GSC01:
    """
    High level functions for GSC01 by sigma koki.
    """
    def __init__(self, port, timeout=10):
        self.port = port
        self.timeout = timeout

    def return_to_origin(self):
        return_to_origin(self.port, self.timeout)
        self.wait_until_ready(timeout=60)
        set_origin(self.port, self.timeout)

    def wait_until_ready(self, timeout=10):
        wait_until_ready(self.port, timeout)

    def move_relative(self, pulses):
        move_relative(pulses, self.port, self.timeout)
        self.wait_until_ready(timeout=60)
    
    def move_absolute(self, pulses):
        move_absolute(pulses, self.port, self.timeout)
        self.wait_until_ready(timeout=60)

    def current_position(self):
        return current_position(self.port, timeout=self.timeout)

    def set_speed(self, 
        minimum_speed=500, maximum_speed=5000, acceleration=200, 
        timeout=10
    ):
        """
        Set speed parameters

        Parameters
        ----------
        minimum speed in [pps]
        maximum speed in [pps]
        acceleration time in [ms]
        """
        set_speed(
            self.port, minimum_speed=minimum_speed, maximum_speed=maximum_speed,
            acceleration=acceleration, timeout=timeout
        )


def return_to_origin(port='/dev/ttyUSB0', timeout=10):
    """
    Returns to the mechanical origin
    """
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write('H:1\r\n'.encode())
        res = ser.readline().decode('utf8').strip()
        if res != 'OK':
            raise IOError('Communication with {} failed.'.format(port))


def wait_until_ready(port='/dev/ttyUSB0', timeout=10):
    with serial.Serial(port, timeout=timeout) as ser:
        now = time.time()
        while time.time() - now < timeout:
            ser.write('!:\r\n'.encode())
            res = ser.readline().decode('utf8').strip()
            if res == 'R':
                break
            time.sleep(0.5)

    if res == 'B':
        raise IOError('Device is still running after {}s.'.format(timeout))


def move_relative(pulses, port='/dev/ttyUSB0', timeout=10):
    """
    Returns to the mechanical origin
    """
    with serial.Serial(port, timeout=timeout) as ser:
        if pulses > 0:
            ser.write('M:1+P{}\r\n'.format(pulses).encode())
        else:
            ser.write('M:1-P{}\r\n'.format(-pulses).encode())
        res = ser.readline().decode('utf8').strip()
        if res != 'OK':
            raise IOError('Communication with {} failed.'.format(port))

        ser.write('G:\r\n'.format(-pulses).encode())
        res = ser.readline().decode('utf8').strip()


def move_absolute(pulses, port='/dev/ttyUSB0', timeout=10):
    """
    Returns to the mechanical origin
    """
    with serial.Serial(port, timeout=timeout) as ser:
        if pulses > 0:
            ser.write('A:1+P{}\r\n'.format(pulses).encode())
        else:
            ser.write('A:1-P{}\r\n'.format(-pulses).encode())
        res = ser.readline().decode('utf8').strip()
        if res != 'OK':
            raise IOError('Communication with {} failed.'.format(port))

        ser.write('G:\r\n'.format(-pulses).encode())
        res = ser.readline().decode('utf8').strip()

def set_origin(port, timeout=10):
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write('R:1\r\n'.encode())
        res = ser.readline().decode('utf8').strip()
        if res != 'OK':
            raise IOError('Communication with {} failed.'.format(port))

def set_speed(
    port, 
    minimum_speed=500, maximum_speed=5000, acceleration=200, 
    timeout=10
):
    """
    Set speed parameters

    Parameters
    ----------
    minimum speed in [pps]
    maximum speed in [pps]
    acceleration time in [ms]
    """
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write('D:S{}F{}R{}\r\n'.format(
            int(minimum_speed), int(maximum_speed), int(acceleration)
        ).encode())
        res = ser.readline().decode('utf8').strip()
        if res != 'OK':
            raise IOError('Communication with {} failed.'.format(port))

def current_position(port, timeout=10):
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write('Q:\r\n'.encode())
        res = ser.readline().decode('utf8').strip()
        return int(res.split(',')[0])
