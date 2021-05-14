import serial
import time


_WAIT_TIME = 0.3  # wait 3 second if not respond


class XA:
    """
    High level functions for XA by sus.
    """
    def __init__(self, port, pno=63, timeout=10):
        """
        port: com port for XA
        pno: arbitrary number in 1 <= pno <= 63
        """
        self.port = port
        self.pno = pno
        self.timeout = timeout

    def return_to_origin(self):
        return_to_origin(self.port)
        wait_until_ready(self.port, timeout)

    def wait_until_ready(self, timeout=10):
        wait_until_ready(self.port, timeout)

    def move_relative(self, pulses):
        pos = self.current_position(timeout=self.timeout)
        move(self.port, self.pno, position=pos + pulses)
        self.wait_until_ready(timeout=60)
    
    def move_absolute(self, pulses):
        move(self.port, self.pno, position=pulses)
        self.wait_until_ready(timeout=60)

    def current_position(self):
        return current_position(self.port, timeout=self.timeout)

    def set_speed(self, 
        speed=None, 
        acceleration=None,
        move_method=None,
        output_config=None,
        pressing_force=None,
        pressing_start=None,
        timeout=10
    ):
        """
        Set speed parameters
        """
        config = read_pno(self.port, self.pno, timeout=10)
        if speed is not None:
            config['speed'] = speed
        if acceleration is not None:
            config['acceleration'] = acceleration
        if move_method is not None:
            config['move_method'] = move_method
        if output_config is not None:
            config['output_config'] = output_config
        if pressing_force is not None:
            config['pressing_force'] = pressing_force
        if pressing_start is not None:
            config['pressing_start'] = pressing_start
        move(self.port, self.pno, **config, time=self.timeout)


def return_to_origin(port, timeout=10):
    """
    Returns to the mechanical origin
    """
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write('OMP00\r\n'.encode())
        res = ser.readline().decode('utf8').strip()


def to_hexstring(
    value, ndigit, name, min_value=None, max_value=None, 
):
    """
    make integer to hex value
    """
    if min_value is not None and value < min_value:
        raise ValueError('{} should be larger than {}. Given {}.'.format(
            name, min_value, value
        ))
    if max_value is not None and value > max_value:
        raise ValueError('{} should be smaller than {}. Given {}.'.format(
            name, max_value, value
        ))

    s = '0' * ndigit + hex(pno)[2:]
    return s[-ndigit:]


def from_hexstring(s):
    return int('0x' + s)


def read_pno(port, pno, timeout=10):
    """
    Returns the current setting from pno
    """    
    pnostring = to_hexstring(pno, 2, 'pno', 1, 63)
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write('ORP{0:2s}\r\n'.format(pno_string).encode())
        res = ser.readline().decode('utf8').strip()

    return {
        'speed': from_hexstring(res[5:9]),
        'acceleration': from_hexstring(res[9]),
        'move_method': from_hexstring(res[10]),
        'position': from_hexstring(res[11:16]),
        'output_config': from_hexstring(res[16]),
        'pressing_force': from_hexstring(res[17:19]),
        'pressing_start': from_hexstring(res[19:21])
    }


def move(
    port, pno, **kwargs, timeout=10
):
    """
    Move to the position with speed and acceleration
    """
    config = read_pno(port, pno, timeout=timeout)
    for key, item in kwargs:
        config[key] = item

    with serial.Serial(port, timeout=timeout) as ser:
        ser.write(
            'OWP' + 
            to_hexstring(config['pno'], 2, 'pno') + 
            to_hexstring(config['speed'], 4, 'speed') + 
            to_hexstring(config['acceleration'], 1, 'acceleration') + 
            to_hexstring(config['move_method'], 1, 'move_method') + 
            to_hexstring(config['position'], 5, 'position') + 
            to_hexstring(config['output_config'], 1, 'output_config') + 
            to_hexstring(config['pressing_force'], 2, 'pressing_force') + 
            to_hexstring(config['pressing_start'], 2, 'pressing_start') + 
            '\r\n'
        )
        res = ser.readline().decode('utf8').strip()
        ser.write(
            'OMP' + to_hexstring(config['pno'], 2, 'pno') + '\r\n'
        )
        res = ser.readline().decode('utf8').strip()


def wait_until_ready(port, timeout=10):
    with serial.Serial(port, timeout=timeout) as ser:
        now = time.time()
        while time.time() - now < timeout:
            ser.write('ORA\r\n'.encode())
            res = ser.readline().decode('utf8').strip()
            if res[3] in ['1', '2']:
                break
            time.sleep(0.5)

    if res[3] == '0':
        raise IOError('Device is still running after {}s.'.format(timeout))


def set_speed(
    port, 
    maximum_speed=30, acceleration=3, 
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
        ser.write('D:1S{}F{}R{}\r\n'.format(
            int(minimum_speed), int(maximum_speed), int(acceleration)
        ).encode())
        res = ser.readline().decode('utf8').strip()
        if res != 'OK':
            raise IOError('Communication with {} failed.'.format(port))


def current_position(port, timeout=10):
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write('ORC\r\n'.encode())
        res = ser.readline().decode('utf8').strip()
        return int(res[3:].strip())
