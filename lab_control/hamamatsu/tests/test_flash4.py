from .. import flash4


def _test_cooler():
    camera = flash4.Flash4(0)
    camera.setCoolerOff()
    
def test_exposure_time():
    camera = flash4.Flash4(0)
    for key, item in camera.getCameraProperties().items():
        print(key, item, camera.getPropertyValue(key))
        print(camera.getPropertyText(key))

    camera.setExposureTime(0.01)