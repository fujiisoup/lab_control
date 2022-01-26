from multiprocessing.sharedctypes import Value
from lab_control.sentech import SentechCamera


def _test_shoot():
    camera = SentechCamera(0)
    camera.configure(BinningVertical=1)
    images = camera.shoot(1, 0.1)
    assert images.shape[0] == 1

    images = camera.shoot(3, 0.1)
    assert images.shape[0] == 3
    camera.__del__()

def test_get_configuration():
    camera = SentechCamera(0)
    camera.get_current_configuration()
    camera.__del__()

def test_shoot_xr():
    camera = SentechCamera(0)
    camera.configure(BinningVertical=1)

    images = camera.shoot(3, 0.1, return_xr=True)
    print(images)
    camera.__del__()



