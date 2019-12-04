# Control scripts for spectrometers

Currently, we support THR640.

## Usage

```python
from lab_control.spectrometer import thr640

thr640.goto('/dev/USB0', 140000)
```