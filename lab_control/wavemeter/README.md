# Control script of Wavemeters 
Currently, we support WA-1000.


## Usage
```python
>>> from lab_control.wavemeter import wa1000
>>> wa1000.get_wavelength('/dev/ttyUSB0')

(771.451, 
 {'UNITS - nm': True, 'UNITS - cm-1': False, 'UNITS - GHz': False, 'DISPLAY - Wavelength': False, 'DISPLAY - Deviation': False, 'MEDIUM - Air': False, 'MEDIUM - Vacuum': False, 'RESOLUTION - Fixed': False, 'RESOLUTION - Auto': False, 'AVERAGING - On': False, 'AVERAGING - Off': False}, 
 {'DISPLAY RES': False, 'SETPOINT': False, '# AVERAGED': False, 'ANALOG RES': False, 'PRESSURE': False, 'TEMPERATURE': False, 'HUMIDITY': False, 'SETUP Restore/Save': False, 'REMOTE': False, 'INPUT ATTENUATOR Auto': False, 'INPUT ATTENUATOR Manual': False})
```