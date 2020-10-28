# About
A small wrapper to control USB-1208LS by measurement computing.inc

Scripts are copied from https://github.com/wjasper/Linux_Drivers/

# Install

## For linux

### Install the some libraries
```
sudo apt-get install libusb-1.0-0-dev libudev-dev
```

### Add a rules in udev
```
# measurement computing devices
SUBSYSTEM=="usb", ATTRS{idVendor}=="09db", ATTRS{idProduct}=="007a", GROUP="mcc"
, MODE="0666"
KERNEL=="hidraw*", ATTRS{idVendor}=="09db", ATTRS{idProduct}=="007a", GROUP="mcc
", MODE="0666"
```

Do not forget to add the user to group `mcc`.

## Python
```
pip install hidapi
pip install libusb1
```

# Windows installation

```
pip mcculw
```