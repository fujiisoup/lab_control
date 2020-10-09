# Control scripts for spectrometers

Currently, we support THR640.

## Usage

```python
from spectrometer import thr640

spectrometer = thr640.THR640()

# gotoで行きたい座標に行く
spectrometer.goto(count=10000)
```
