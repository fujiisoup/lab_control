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

  # test wrapper
  val = device.AIn_single_ended(0)
  val = device.AIn_differential(0, 10.0)
  assert isinstance(val, float)

def test_AInScan():
  device = usb_1208LS()

  nQueue = 4    # depth of the queue: must be 1, 2, 4 or 8
  chanQueue = [0, 1, 2, 3, 0, 1, 2, 3]
  gain = usb_1208LS.BP_10_00V
  gainQueue = [gain, gain, gain, gain, gain, gain, gain, gain]
  frequency = 150   # 150 Hz
  count = 96        # must be an even number
  options = usb_1208LS.AIN_EXECUTION | usb_1208LS.AIN_BURST_MODE
  value = device.AInScan(count, frequency, nQueue, chanQueue, gainQueue, options)
  print('Total number of samples = ', len(value))
  for i in range(int(count/4)):
    print('scan ',i, end=' ')
    for j in range(4):
      print(format(device.volts(gain,value[4*i+j]),'.2f'),end=' ')
  raise ValueError

def testAout():
  device = usb_1208LS()
  device.AOut(0, 0x300)
  device.AOut(1, 0x300)

  device.AO(0, 3.0)
  device.AO(0, 5.0)
