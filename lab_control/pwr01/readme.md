# Control scripts for [PWR-01](https://www.kikusui.co.jp/en/product/detail.php?IdFamily=0143), a DC power supply by Kikusui

## using in Ubuntu

### Requirement

+ python-usbtmc  
```
pip install python-usbtmc
```

+ pyusb
```
pip install pyusb
```

### Preparation

Create a text file (if not exist) in '/etc/udev/rules.d/usbtmc.rules'

Write the following in the file and save it.
```
# USBTMC instruments
# Kikusui Electronics Corp.
SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="0b3e", ATTRS{idProduct}=="10
49", GROUP="usbtmc", MODE="0660"
```

Add a usergroup `usbtmc`
```
sudo groupadd usbtmc
sudo usermod [your username] -G usbtmc
```

Restart the computer.

For the details, see
http://alexforencich.com/wiki/en/python-usbtmc/readme



## using in Windows

### Requirement

+ python-usbtmc  
```
pip install python-usbtmc
```

+ pyusb
```
pip install pyusb
```

### preparation

Download Zadig from
http://zadig.akeo.ie/
and execute Zadig

Choose libusb-win32(vX.X.X.X) in Zadig, then install