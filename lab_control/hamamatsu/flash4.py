"""
More user friendly version of hamamatsu.py
"""
import time
from .hamamatsu import HamamatsuCamera


class Flash4(HamamatsuCamera):
    def _setProperty(self, key, value, max_wait_time=1):
        self.setPropertyValue(key, value)
        start = time.time()
        self.setPropertyValue(key, value)
        while time.time() < start + max_wait_time:
            actual = self.getPropertyValue(key)[0]
            if actual == value:
                return
        
        raise ValueError('{} is not set. Now {}'.format(
            key,
            self.getPropertyValue('timing_exposure')[0]))
    
    def setCoolerOn(self):
        self._setProperty('sensor_cooler_status', 0)

    def setCoolerOff(self):
        self._setProperty('sensor_cooler_status', 1)

    def setExposureTime(self, time_in_second):
        """
        Set an exposure time in second
        """
        time_in_ms = int(time_in_second * 1000)
        self._setProperty('exposure_time', time_in_ms)

        

