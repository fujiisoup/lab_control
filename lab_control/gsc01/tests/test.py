from .. import gsc01


def test():
    # return to origin
    gsc01.return_to_origin(port='/dev/ttyUSB0', timeout=1)
    
    gsc01.wait_until_ready(port='/dev/ttyUSB0', timeout=10)
    # go relative pulse
    gsc01.move_relative(-10000, port='/dev/ttyUSB0', timeout=1)
    gsc01.wait_until_ready(port='/dev/ttyUSB0', timeout=10)
    gsc01.move_relative(3000, port='/dev/ttyUSB0', timeout=1)
    gsc01.wait_until_ready(port='/dev/ttyUSB0', timeout=10)

    # go absolute pulse
    gsc01.move_relative(10000, port='/dev/ttyUSB0', timeout=1)
    gsc01.wait_until_ready(port='/dev/ttyUSB0', timeout=10)
    gsc01.move_relative(3000, port='/dev/ttyUSB0', timeout=1)
    gsc01.wait_until_ready(port='/dev/ttyUSB0', timeout=10)


def test_GSC01():
    # return to origin
    gsc = gsc01.GSC01(port='/dev/ttyUSB0', timeout=1)
    gsc.return_to_origin()
    gsc.move_absolute(100)
    gsc.move_absolute(-100)