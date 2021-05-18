import numpy as np
from . import xa


def _test_origin():
    # return to origin
    xa.return_to_origin('/dev/ttyUSB0')
    xa.wait_until_ready('/dev/ttyUSB0')


def test_highlevel():
    device = xa.XA_U1(port='/dev/ttyUSB0')
    device.return_to_origin()

    pulses = [10000, 100, 200]
    for pulse in pulses:
        device.move_absolute(pulse)
        # device.move_relative(10000)
        assert np.allclose(pulse, device.current_position(), atol=1)
