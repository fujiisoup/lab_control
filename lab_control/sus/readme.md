# Controllers for SUS stages.

See 
https://fa.sus.co.jp/products/xa/software/xa_manual/
for the details.

## required package

+ pyseiral

## Usage

```python
# port. For linux, something like '/dev/ttyUSB0'
# Windows, e.g., 'COM3'
device = sus.XA_U1(port='/dev/ttyUSB0')

# return to the machine origin
device.return_to_origin()

# move to position 10000
device.move_absolute(10000)

# move to position 10000
device.set_speed(10)  # change speed to 10
```