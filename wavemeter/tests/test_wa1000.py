from .. import wa1000


def test_get_wavelength():
    # working test
    wa1000.get_wavelength(port='/dev/ttyUSB0', timeout=10)
    