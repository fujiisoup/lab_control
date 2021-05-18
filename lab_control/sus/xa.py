import serial
import time


_WAIT_TIME = 0.3  # wait 3 second if not respond
    

class XA_U1:
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
        # set default speed
        config = {
            'speed': 10,
            'acceleration': 1,
            'move_method': 1,
            'output_config': 0,
            'pressing_force': 30,
            'pressing_start': 10, 
            'position': current_position(self.port, timeout=self.timeout)
        }
        write_pno(self.port, self.pno, config, self.timeout)


    def return_to_origin(self):
        return_to_origin(self.port)
        self.wait_until_ready(timeout=60)

    def wait_until_ready(self, timeout=10):
        wait_until_ready(self.port, timeout)

    def move_relative(self, pulses):
        pos = self.current_position()
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
        pressing_start=None
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


def handle_alarm(code, port=None, reset=True):
    """
    Handles alarm by XA series.
    if reset is True, the error is always reset after received.
    """
    code = code.strip()
    if code[:3] != '0%%':
        return ## no error
    code = code[3:]

    if code[0] == '1':
        raise IOError('EEPROM error is returned. Check the hardware.')
    error_code = code[2]

    if error_code == '1':
        if reset:
            reset_alarm(port)
        raise IOError("Communication error. {}".format(code))
    elif error_code == '2':
        if reset:
            reset_alarm(port)
        raise IOError("Limit switch is ON. {}".format(code))
    elif error_code == '3':
        if reset:
            reset_alarm(port)
        raise IOError("The origin is not yet recovered. {}".format(code))
    elif error_code == '4':
        if reset:
            reset_alarm(port)
        raise IOError("Large deviation error. {}".format(code))
    elif error_code == '5':
        if reset:
            reset_alarm(port)
        raise IOError("Invalid value in the given position. {}".format(code))
    elif error_code == '6':
        if reset:
            reset_alarm(port)
        raise IOError("Invalid value in the given speed. {}".format(code))
    elif error_code == '7':
        if reset:
            reset_alarm(port)
        raise IOError("Invalid value in the given acceleration. {}".format(code))
    elif error_code == '8':
        if reset:
            reset_alarm(port)
        raise IOError("Invalid value. {}".format(code))
    elif error_code == 'F':
        if reset:
            reset_alarm(port)
        raise IOError("Emergency stop. {}".format(code))
    

def reset_alarm(port):
    with serial.Serial(port, timeout=10) as ser:
        ser.write('0AR\r\n'.encode())
        

def return_to_origin(port, timeout=10, reset_alarm=True):
    """
    Returns to the mechanical origin
    """
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write('0MP00\r\n'.encode())
        res = ser.readline().decode('utf8').strip()
        handle_alarm(res, port=port, reset=reset_alarm)


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

    s = hex(value)[2:]
    if len(s) > ndigit:
        raise ValueError('The given value {} has more than the allowed digit {}.'.format(value, ndigit))
    s = '0' * ndigit + s
    return s[-ndigit:].upper()


def from_hexstring(s):
    return int('0x' + s, base=16)


def read_pno(port, pno, timeout=10, reset_alarm=True):
    """
    Returns the current setting from pno
    """    
    pnostring = to_hexstring(pno, 2, 'pno', 1, 63)
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write('0RP{0:2s}\r\n'.format(pnostring).encode())
        res = ser.readline().decode('utf8').strip()
        handle_alarm(res, port=port, reset=reset_alarm)
        
    return {
        'speed': from_hexstring(res[5:9]),
        'acceleration': from_hexstring(res[9]),
        'move_method': from_hexstring(res[10]),
        'position': from_hexstring(res[11:16]),
        'output_config': from_hexstring(res[16]),
        'pressing_force': from_hexstring(res[17:19]),
        'pressing_start': from_hexstring(res[19:21])
    }


def write_pno(port, pno, config, timeout):
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write((
            '0WP' + 
            to_hexstring(pno, 2, 'pno') + 
            to_hexstring(config['speed'], 4, 'speed') + 
            to_hexstring(config['acceleration'], 1, 'acceleration') + 
            to_hexstring(config['move_method'], 1, 'move_method') + 
            to_hexstring(config['position'], 5, 'position') + 
            to_hexstring(config['output_config'], 1, 'output_config') + 
            to_hexstring(config['pressing_force'], 2, 'pressing_force') + 
            to_hexstring(config['pressing_start'], 2, 'pressing_start') + 
            '\r\n'
        ).encode())
        res = ser.readline().decode('utf8').strip()
        handle_alarm(res, port=port, reset=reset_alarm)


def move(port, pno, **kwargs):
    """
    Move to the position with speed and acceleration
    """
    timeout = kwargs.get('timeout', 10)
    reset_alarm = kwargs.get('reset_alarm', True)
    config = read_pno(port, pno, timeout=timeout)

    for key, item in kwargs.items():
        config[key] = item
    
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write((
            '0MV' + 
            to_hexstring(config['speed'], 4, 'speed') + 
            to_hexstring(config['acceleration'], 1, 'acceleration') + 
            to_hexstring(config['move_method'], 1, 'move_method') + 
            to_hexstring(config['position'], 5, 'position') + 
            '\r\n'
        ).encode())
        res = ser.readline().decode('utf8').strip()
        handle_alarm(res, port=port, reset=reset_alarm)


def wait_until_ready(port, timeout=10, reset_alarm=True):
    with serial.Serial(port, timeout=timeout) as ser:
        now = time.time()
        while time.time() - now < timeout:
            ser.write('0RA\r\n'.encode())
            res = ser.readline().decode('utf8').strip()
            handle_alarm(res, port=port, reset=reset_alarm)
            if res[3] in ['1', '2']:
                break
            time.sleep(0.5)

    if res[3] == '0':
        raise IOError('Device is still running after {}s.'.format(timeout))


def current_position(port, timeout=10, reset_alarm=True):
    with serial.Serial(port, timeout=timeout) as ser:
        ser.write('0RC\r\n'.encode())
        res = ser.readline().decode('utf8').strip()
        handle_alarm(res, port=port, reset=reset_alarm)
        return int(res[3:].strip(), base=16)
