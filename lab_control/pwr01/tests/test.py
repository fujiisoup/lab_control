import time
import numpy as np
import usbtmc
from lab_control import pwr01


def test_on():
    instr = pwr01.PWR01()
    instr.reset()
    instr.set_voltage(100)
    instr.set_current(1.0)
    instr.output_on(max_time=1.0)

    current = instr.get_current()
    voltage = instr.get_voltage()
    assert np.allclose(voltage, 100, atol=5.0)

    # change voltage
    instr.set_voltage(200)
    time.sleep(0.2)
    assert instr.is_on
    voltage = instr.get_voltage()
    assert np.allclose(voltage, 200, atol=5.0)

    instr.output_off(max_time=1.0)
    assert instr.is_off
    

def test_set_voltage():
    instr = pwr01.PWR01()
    instr.reset()
    instr.set_voltage(100)
    # make sure it does not turn on the output
    assert instr.is_off
    time.sleep(0.5)
    assert instr.is_off
    