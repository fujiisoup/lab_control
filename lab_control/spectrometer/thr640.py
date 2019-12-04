import configparser
import time
import numpy as np
import serial


class THR640:
    def __init__(self, port='/dev/ttyUSB0', config_file=None):
        self._port = port
        if config_file is None:
            self._config = None
        else:
            self._config = configparser.ConfigParser()
            self._config.open(config_file)

    def goto(self, count=None, wavelength=None):
        """
        Move the moter to the required position.
        Wait until the movement finishes.
        """
        if count is None and wavelength is None:
            raise ValueError('Either of count and wavelength should be given.')
            
        if count is None:
            count = self._wavelength_to_count(wavelength)

        while not self._check_ready():
            self._send_goto_count(count)
            time.sleep(1)

    def _check_ready(self):
        """ returns if the spectrometer is ready """
        raise NotImplementedError

    def _send_goto_count(self, count):
        """ send a command to go to the specified count """
        raise NotImplementedError

    def _wavelength_to_count(self, wavelength):
        if self._config is None:
            raise ValueError('Requires a configuration file to compute wavelength.')
        
        order = self._config['calibration']['order']
        coef = [self._config['calibration']['coefficient{}'.format(o)] 
                for o in range(order)][::-1]
        return np.polyval(coef, x=count)