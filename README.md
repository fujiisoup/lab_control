# Control scripts for experiment in Fujii team

## Install

In this scripts, we will use serial port.
We need some drivers for it,

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

## Python packages
+ pyserial
```
conda install pyserial
```
