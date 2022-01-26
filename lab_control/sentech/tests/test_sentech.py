import numpy as np
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

    images = camera.shoot(3, 0.1, return_xr=True)
    camera.__del__()

def test_shoot_exposure():
    camera = SentechCamera(0)
    images = camera.shoot(3, 0.1, return_xr=True)
    assert np.allclose(np.diff(images['time'].values), 0.1, rtol=1e-4)

    images = camera.shoot(3, 0.3, return_xr=True)
    assert np.allclose(np.diff(images['time'].values), 0.3, rtol=1e-4)
    
    camera.__del__()


