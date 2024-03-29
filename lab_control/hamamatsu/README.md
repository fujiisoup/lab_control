# Module for Hamamatsu flash4

## Requirement 

DCAM should be installed, which is shipped with hamamatsu software

## Usage

```python
from lab_control import hamamatsu

camera = hamamatsu.Flash4(0)
data = camera.shoot(num_frames=1, exposure_time=0.1)
```

## Possible properties

- sensor_mode [1, 'MODE']
- colortype [1, 'MODE']
- bit_per_channel [16, 'LONG']
- trigger_source [1, 'MODE']
- trigger_mode [1, 'MODE']
- trigger_active [1, 'MODE']
- trigger_polarity [1, 'MODE']
- trigger_connector [2, 'MODE']
- trigger_times [1, 'LONG']
- trigger_delay [0.0, 'REAL']
- sensor_cooler_status [2, 'MODE']
- exposure_time [0.009997714285714285, 'REAL']
- defect_correct_mode [2, 'MODE']
- binning [1, 'MODE']
- subarray_hpos [0, 'LONG']
- subarray_hsize [2048, 'LONG']
- subarray_vpos [0, 'LONG']
- subarray_vsize [2048, 'LONG']
- subarray_mode [1, 'MODE']
- timing_readout_time [0.009997714285714285, 'REAL']
- timing_cyclic_trigger_period [0.0, 'REAL']
- timing_min_trigger_blanking [0.009997714285714285, 'REAL']
- timing_min_trigger_interval [0.019995432857142857, 'REAL']
- timing_global_exposure_delay [0.00999771857142857, 'REAL']
- timing_exposure [3, 'MODE']
- timing_invalid_exposure_period [4.2857142851931984e-09, 'REAL']
- internal_frame_rate [100.02286236854138, 'REAL']
- internal_frame_interval [0.009997714285714285, 'REAL']
- image_width [2048, 'LONG']
- image_height [2048, 'LONG']
- image_rowbytes [4096, 'LONG']
- image_framebytes [8388608, 'LONG']
- image_top_offset_bytes [0, 'LONG']
- image_pixel_type [2, 'MODE']
- number_of_output_trigger_connector [3, 'LONG']
- output_trigger_polarity[0] [1, 'MODE']
- output_trigger_active[0] [1, 'MODE']
- output_trigger_delay[0] [0.0, 'REAL']
- output_trigger_period[0] [0.001, 'REAL']
- output_trigger_kind[0] [4, 'MODE']
- system_alive [2, 'MODE']