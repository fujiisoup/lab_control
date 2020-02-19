import time
import usbtmc
from lab_control import pwr01


def test_connection():
    instr = pwr01.PWR01()
    instr.reset()
    instr.set_voltage(100)
    instr.set_current(1.0)
    instr.output_on()
    time.sleep(0.5)
    assert instr.is_on

    instr.output_off()
    time.sleep(0.5)
    assert instr.is_off
    
