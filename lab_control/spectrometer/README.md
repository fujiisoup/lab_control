# Control scripts for spectrometers

Currently, we support THR640.

## Usage

```python
from lab_control.spectrometer import THR640

spectrometer = THR640('/dev/USB0')
spectrometer.goto(count=140000)
```
