"""
More user friendly version of hamamatsu.py
"""
import time
import numpy as np
from .hamamatsu import HamamatsuCamera


class Flash4(HamamatsuCamera):
    def _setProperty(self, key, value, max_wait_time=1, approx=False):
        self.setPropertyValue(key, value)
        start = time.time()
        self.setPropertyValue(key, value)
        while time.time() < start + max_wait_time:
            actual = self.getPropertyValue(key)[0]
            if approx:
                if np.allclose(actual, value, rtol=1e-3):
                    return
            if actual == value:
                return
            time.sleep(0.1)
        
        raise ValueError('{} is not set. Now {}'.format(
            key,
            self.getPropertyValue(key)[0]))

    @property
    def isCoolerOn(self):
        return self.getPropertyValue('sensor_cooler_status')[0] == 2

    def setExposureTime(self, time_in_second):
        """
        Set an exposure time in second
        """
        self._setProperty('exposure_time', time_in_second, approx=True)

    @property    
    def exposureTime(self):
        return self.getPropertyValue('exposure_time')[0]

    @property
    def frameInterval(self):
        return self.getPropertyValue('internal_frame_interval')[0]

    @property
    def frameRate(self): 
        return self.getPropertyValue('internal_frame_rate')[0]

    def __del__(self):
        self.shutdown()    

    def shoot(self, num_frames=1, exposure_time=None):
        """
        A high level method to shoot photos and load into memory.

        num_frames: number of frames
        exposure_time: exposure_time in second. If None, the current value is used.
        """
        if exposure_time is not None:
            self.setExposureTime(exposure_time)
        
        jitter = 0.3
        time_wait = self.frameInterval * num_frames + jitter
        buffer_time = max([time_wait, 2.0])
        self.startAcquisition(buffer_time=buffer_time)

        n_processed = 0
        data = []
        while n_processed < num_frames:
            time.sleep(time_wait)
            frames = self.getFrames()
            if len(frames) > 0:
                frames, (x, y) = frames
                # crop if there are more
                frames = frames[:num_frames - n_processed]

                data += [f.getData().astype(np.int32).reshape(x, y) for f in frames]
                n_processed = len(data)
                print(n_processed)
        self.stopAcquisition()
        return np.stack(data[:num_frames], axis=0)