import time
from lab_control import hamamatsu


def test_cooler():
    camera = hamamatsu.Flash4(0)
    # assert camera.isCoolerOn
    props = camera.getCameraProperties() 
    assert camera.isCoolerOn
    camera.shutdown()
    
def test_exposure_time():
    camera = hamamatsu.Flash4(0)
    for key, item in camera.getCameraProperties().items():
        print(key, item, camera.getPropertyValue(key))
        print(camera.getPropertyText(key))

    camera.setExposureTime(0.01)
    camera.shutdown()

def test_shoot():
    camera = hamamatsu.Flash4(0)
    for frame, exposure in [(2, 0.02), (2, 1.2), (150, 0.01)]:
        start = time.time()
        data = camera.shoot(frame, exposure)
        stop = time.time()
        assert len(data) == frame
        assert stop - start < (frame * (exposure + 0.03) + 1.0)
    camera.shutdown()
