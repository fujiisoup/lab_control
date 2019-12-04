import os
from .. import THR640


THISDIR = os.path.dirname(os.path.realpath(__file__))

def test_thr640():
    # working test
    thr640 = THR640('/dev/ttyUSB0')
    thr640.goto(count=10000)
    # forward
    thr640.goto(count=10100)
    # backward
    thr640.goto(count=10000)

    # with config file
    thr640 = THR640('/dev/ttyUSB0', config_file=THISDIR + '/../thr640_config.ini')
    thr640.goto(wavelength=400)

