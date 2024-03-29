# A wrapper of usb_1208LS.py
import numpy as np
from . import usb_1208LS


class usb_1208LS(usb_1208LS.usb_1208LS):
    def AIn_single_ended(self, ch):
        """
        Analog input with single-ended configuration.
        ch must be one of 0 ~ 7
        """
        value = self.AIn(ch, self.SE_10_00V)
        return self.volts(self.SE_10_00V, value)

    def AIn_differential(self, ch, gain):
        """
        Analog input with differential configuration.
        ch must be one of 0 ~ 3
        Gain must be one of [1.0, 1.25, 2.0, 2.5, 4.0, 5.0, 10.0, 20.0]
        """
        if gain <= 1.0:
            gain = self.BP_1_00V
        elif gain <= 1.25:
            gain = self.BP_1_25V
        elif gain <= 2.0:
            gain = self.BP_2_00V
        elif gain <= 2.5:
            gain = self.BP_2_50V
        elif gain <= 4.0:
            gain = self.BP_4_00V
        elif gain <= 5.0:
            gain = self.BP_5_00V
        elif gain <= 10.0:
            gain = self.BP_10_00V
        elif gain <= 20.0:
            gain = self.BP_20_00V
        else:
            raise ValueError('gain must be in one of [1.0, 1.25, 2.0, 2.5, 4.0, 5.0, 10.0, 20.0].' + 
                             'given {}.'.format(gain))
        value = self.AIn(ch, gain)
        return self.volts(gain, value)

    def AO(self, ch, value):
        """
        Analog output
        ch should be one of 0 or 1
        value should be within 0 ~ 5 V.
        """
        volt = int(value / 5.0 * 0x3ff)
        self.AOut(0, volt)
        
    def __del__(self):
        self.h.close()