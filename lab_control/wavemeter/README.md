# Control script of Wavemeters 
Currently, we support WA-1000.

##  Install
### Ubuntu
Install [ftdi driver](https://www.ftdichip.com/Drivers/D2XX.htm)

+ libusb-1.0  `apt-get install libusb-1.0`
+ create `/etc/udev/rules.d/11-ftdi.rules`

If you got an error, Permission denied, see https://stackoverflow.com/questions/27858041/oserror-errno-13-permission-denied-dev-ttyacm0-using-pyserial-from-pyth

Find the COM port
```
dmesg | grep tty
```
It should be like `/dev/ttyUSB0`

### Windows
Install [ftdi driver](https://www.ftdichip.com/Drivers/D2XX.htm)

Find the COM port. It will look like `COM3`

## Python package
+ pyserial
```
conda install pyserial
```

## Usage
```python
>>> from lab_control.wavemeter import wa1000
>>> wa1000.get_wavelength('/dev/ttyUSB0')

(771.451, 
 {'UNITS - nm': True, 'UNITS - cm-1': False, 'UNITS - GHz': False, 'DISPLAY - Wavelength': False, 'DISPLAY - Deviation': False, 'MEDIUM - Air': False, 'MEDIUM - Vacuum': False, 'RESOLUTION - Fixed': False, 'RESOLUTION - Auto': False, 'AVERAGING - On': False, 'AVERAGING - Off': False}, 
 {'DISPLAY RES': False, 'SETPOINT': False, '# AVERAGED': False, 'ANALOG RES': False, 'PRESSURE': False, 'TEMPERATURE': False, 'HUMIDITY': False, 'SETUP Restore/Save': False, 'REMOTE': False, 'INPUT ATTENUATOR Auto': False, 'INPUT ATTENUATOR Manual': False})
```