# Control scripts for experiment in Fujii team

## Installing USB-RS232C convertors

In this scripts, we will use serial port.
We need some package and drivers for it,

## Python packages
+ pyserial
```
conda install pyserial
```

### Ubuntu
Install [ftdi driver](https://www.ftdichip.com/Drivers/D2XX.htm)

+ libusb-1.0  `apt-get install libusb-1.0`

#### With ftdi device
+ create `/etc/udev/rules.d/11-ftdi.rules`

#### With PL2303 device
Find the manufacturer ID and product ID 
```bash
lsusb
```
It shows something like the following

> Bus 002 Device 005: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port

In this case, the manufacturer ID is 067b and product ID is 2303.

Create a file `/etc/udev/rules.d/pl2303.rules` and add the following line

```
# PL2302 USB2.0-RS232 convertor
SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", GROUP="usbtmc", MODE="0660"
```

Then, restart.


### Windows

#### Install python packages
```python
pip install hidapi
pip install libusb1
```

### install binary snapshot for libusb1
Download 
libusb-1.0.dll
from
http://sourceforge.net/projects/libusb/files/
and save it in 
C:\Windows\System32

See 
https://github.com/libusb/libusb/wiki/Windows
for the details.

### Usage

Find the COM port
```
dmesg | grep tty
```
It should be like `/dev/ttyUSB0`

### Windows
Install [ftdi driver](https://www.ftdichip.com/Drivers/D2XX.htm)

Find the COM port. It will look like `COM3`

