# A wrapper of usb_1208LS.py
import numpy as np
import time


try:
    from mcculw import ul
    from mcculw.enums import ULRange
    from mcculw.ul import ULError
    HAS_MCCULW = True
except OSError as e:
    raise ImportError(e)
except ImportError:
    from . import usb_1208LS
    HAS_MCCULW = False


NUM_TRIAL = 128


class usb_1208LS:
    def __init__(self):
        if not HAS_MCCULW:
            raise ImportError(
                'mcculw is necessary to drive usb_1208LS in windows. '
                'do "pip install mcculw"')
        # TODO maybe there will be more than one board.
        self.board_num = 0 

    def AIn_single_ended(self, ch):
        """
        Analog input with single-ended configuration.
        ch must be one of 0 ~ 7
        """
        if ch not in range(8):
            raise ValueError('Invalid channel: {}'.format(ch))
        ai_range = ULRange.BIP10VOLTS
        for trial in range(NUM_TRIAL):
            try:
                return ul.to_eng_units(
                    self.board_num,
                    ai_range, ul.a_in(self.board_num, ch, ai_range))
            except ULError as e:
                if trial == NUM_TRIAL - 1:
                    raise e
                print('waiting for ADC')
                time.sleep(0.1)

    def AIn_differential(self, ch, gain):
        """
        Analog input with differential configuration.
        ch must be one of 0 ~ 3
        Gain must be one of [1.0, 1.25, 2.0, 2.5, 4.0, 5.0, 10.0, 20.0]
        """
        raise NotImplementedError

    def AO(self, ch, value):
        """
        Analog output
        ch should be one of 0 or 1
        value should be within 0 ~ 5 V.
        """
        if ch not in range(2):
            raise ValueError('Invalid channel: {}'.format(ch))
        if value < 0.0 or value > 5.0:
            raise ValueError('Output should be in 0--5 V')

        ao_range = ULRange.UNI5VOLTS
        value = ul.from_eng_units(self.board_num, ao_range, value)
        
        for trial in range(NUM_TRIAL):
            try:
                ul.a_out(self.board_num, ch, ao_range, value)
            except ULError as e:
                if trial == NUM_TRIAL - 1:
                    raise e
                print('waiting for ADC')
                time.sleep(0.1)
