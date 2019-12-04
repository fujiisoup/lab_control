import serial
import time


_WAIT_TIME = 3  # wait 3 second if not respond
COMMANDS = {'Broadcast': '@\x42\r\n',
            'Save': '@\x0E\r\n',
            'Reset': '@\x0F\r\n',
            'Manual Deattenuate': '@\x10\r\n',
            'Manual Attenuate': '@\x11\r\n',
            'Auto Attenuate': '@\x13\r\n',
            'Humidity': '@\x20\r\n',
            'Pressure': '@\x21\r\n',
            'Temperature': '@\x22\r\n',
            '# Averaged': '@\x23\r\n',
            'Analog Res': '@\x24\r\n',
            'Display Res': '@\x25\r\n',
            'Setpoint': '@\x26\r\n',
            'Units': '@\x27\r\n',
            'Display': '@\x28\r\n',
            'Medium': '@\x29\r\n',
            'Resolution': '@\x2A\r\n',
            'Averaging': '@\x2B\r\n'
}

DISPLAY_MASKS = {
    'UNITS - nm': 0x0009,
    'UNITS - cm-1': 0x0012,
    'UNITS - GHz': 0x0024,
    'DISPLAY - Wavelength': 0x0040,
    'DISPLAY - Deviation': 0x0080,
    'MEDIUM - Air': 0x0100,
    'MEDIUM - Vacuum': 0x0200,
    'RESOLUTION - Fixed': 0x0400,
    'RESOLUTION - Auto': 0x0800,
    'AVERAGING - On': 0x1000,
    'AVERAGING - Off': 0x2000
}
STATUS_MASKS = {
    'DISPLAY RES': 0x0001,
    'SETPOINT': 0x0002,
    '# AVERAGED': 0x0004,
    'ANALOG RES': 0x0008,
    'PRESSURE': 0x0010,
    'TEMPERATURE': 0x0020,
    'HUMIDITY': 0x0040,
    'SETUP Restore/Save': 0x0080,
    'REMOTE': 0x0100,
    'INPUT ATTENUATOR Auto': 0x0200,
    'INPUT ATTENUATOR Manual': 0x0400,
}


def get_wavelength(port='/dev/ttyUSB0', timeout=10):
    """
    """
    res = ''
    now = time.time()
    with serial.Serial(port) as ser: # open serial port 
        while time.time() < now + timeout:
            res = ser.readline()
            if len(res) < 23:
                time.sleep(_WAIT_TIME)
            else:
                return get_status(res)


def get_status(status_string):
    """
    Get the current status
    """
    wavelength, display, status = status_string.decode('utf-8').split(',')
    wavelength = float(wavelength)
    display = int(display)
    status = int(status)
    print(bin(display))
    print(bin(status))
    display = {k: (display & v) == 1 for k, v in DISPLAY_MASKS.items()}
    status = {k: (status & v) == 1 for k, v in STATUS_MASKS.items()}
    return wavelength, display, status


def _set(command):
    # TODO
    while time.time() < now + timeout:
        res = ser.write()
        if res == '4':
            return
    raise TimeoutError('Time out when sending {}.'.format(command))