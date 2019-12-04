# Control script of wavemeter WA-1000

## Requirement

Requires

### OS side
See https://eblot.github.io/pyftdi/installation.html

+ libusb-1.0  `apt-get install libusb-1.0`
+ create `/etc/udev/rules.d/11-ftdi.rules`

If you got an error, Permission denied, see https://stackoverflow.com/questions/27858041/oserror-errno-13-permission-denied-dev-ttyacm0-using-pyserial-from-pyth

etc.

### Python package
+ pyfdti https://eblot.github.io/pyftdi/


## Usage