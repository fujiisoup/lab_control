import os
import thr640
import time

# THISDIR = os.path.dirname(os.path.realpath(__file__))

def test_thr640():
    # working test
    thr = thr640.THR640()
    thr.goto(count=-137000)
    thr.goto(count=-91000)
    thr.goto(count=-120000)
    # # with config file
    # thr640 = THR640('/dev/ttyUSB0', config_file=THISDIR + '/../thr640_config.ini')
    # thr640.goto(wavelength=400)

def test_getlines():
    thr = thr640.THR640()
    thr.get_configuration()

if __name__ == '__main__':
    test_thr640()
