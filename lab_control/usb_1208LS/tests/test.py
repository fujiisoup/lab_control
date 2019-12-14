import pytest
from .. import usb_1208LS
import time


def test_Ai():
  device = usb_1208LS()
  # ch 0, 1, ..., single ended  
  device.AIn(0, usb_1208LS.SE_10_00V)
  device.AIn(3, usb_1208LS.SE_10_00V)
  
  # ch 0, 1, ..., differential
  device.AIn(0, usb_1208LS.BP_20_00V)
  device.AIn(1, usb_1208LS.BP_20_00V)
  device.AIn(1, usb_1208LS.BP_1_00V)


def test_AInScan():
  device = usb_1208LS()
  # ch 0, 1, ..., single ended  
  device.AInScan(0, count=1000, frequency=2000, )
