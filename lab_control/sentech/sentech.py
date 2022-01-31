import time
import sys
import datetime
import numpy as np
from harvesters.core import Harvester

try:
    import xarray as xr
    HAS_XARRAY = True
except ImportError:
    HAS_XARRAY = False


def _default_cti_filepath():
    # its win32, maybe there is win64 too?
    is_windows = sys.platform.startswith('win')
    if is_windows:
        return "C:/Program Files/Common Files/OMRON_SENTECH/GenTL/v1_5/StGenTL_MD_VC141_v1_5.cti" 
    # linux
    return "/opt/sentech/lib/libstgentl.cti"


class SentechCamera:
    def __init__(
        self, camera_index=None, camera_name=None, cti_filepath=None, 
    ):
        """
        A small wrapper of Harvester to use Sentech camera
        cti_filepath: path to cti file.
            In ubunt, the default is /opt/sentech/lib/libstgentl.cti
        """
        if cti_filepath is None:
            cti_filepath = _default_cti_filepath()

        self.h = Harvester()
        self.h.add_file(cti_filepath)
        self.h.update()

        if camera_index is None:
            if camera_name is None:
                raise ValueError(
                    'Either of camera_index or camera_name must be provided.'
                )
            ids = [dev[0] for dev in self.h.device_info_list]
            for i, name in enumerate(ids):
                if name == camera_name:
                    camera_index = i
            if camera_index is None:
                raise ValueError(
                    "No cameras have name {}. The detected cameras are {}".format(
                        camera_name, ids
                    )
                )
        self.camera_index = camera_index
        self.configure_default()
        self.node_map = self._list_node_map()
    
    def configure_default(self):
        """ default settings. Override if necessary """
        self.configure(
            AcquisitionFrameRate=5,
            BinningHorizontalMode='Sum',
            BinningHorizontal=1,
            BinningVerticalMode='Sum',
            BinningVertical=1,
            DecimationHorizontal=1,
            DecimationVertical=1,
            PixelFormat='Mono12',
            ReverseX='False', ReverseY='False',
            TriggerSelector='FrameStart',
            TriggerMode='Off',
            ExposureMode='Off', ExposureTimeSelector='Common', 
            ExposureAuto='Off',
            GainSelector='AnalogAll', Gain=0.0, GainAuto='Off',
            BlackLevelSelector='AnalogAll', BlackLevel=0.0, Gamma=1.0,
        )

    def _list_node_map(self):
        nodes = []
        with self.h.create_image_acquirer(self.camera_index) as ia:
            for m in dir(ia.remote_device.node_map):
                try:
                    if (
                        m[0] != '_' and 
                        hasattr(getattr(ia.remote_device.node_map, m), 'value')
                    ):
                        nodes.append(m)
                except Exception:
                    pass
        return nodes                    
        
    def configure(self, **kwargs):
        """
        Configure the camera. 

        Parameters
        ----------
        bin_horizontal, bin_vertical: bin size
        gain: analog gain
        exposure_time: exposure time in sec

        for other possible keywords, see self.node_map
        """
        with self.h.create_image_acquirer(self.camera_index) as ia:
            for key, value in kwargs.items():
                getattr(ia.remote_device.node_map, key).value = value

    def get_current_configuration(self):
        config = {}
        with self.h.create_image_acquirer(self.camera_index) as ia:
            for key in self.node_map:
                config[key] = getattr(ia.remote_device.node_map, key).value
        return config        

    def shoot(
        self, num_frames=1, exposure_time=None, timeout=10.0, return_xr=False
    ):
        """
        A high level method to shoot photos and load into memory.

        num_frames: number of frames
        exposure_time: exposure_time in second. If None, the current value is used.
        timeout: maximum execution time
        return_xr: if True, returns xr.DataArray object
        """
        frame_rate = 1 / exposure_time
        self.configure(AcquisitionFrameRate=frame_rate)
        content = []
        timestamps = []
        start_datetime = datetime.datetime.now()
        with self.h.create_image_acquirer(self.camera_index) as ia:
            ia.start_acquisition()
            start_time = time.time()
            while (
                len(content) < num_frames and time.time() - start_time < timeout
            ):
                with ia.fetch_buffer() as buffer:
                    payload = buffer.payload
                    component = payload.components[0]
                    width = component.width
                    height = component.height
                    data_format = component.data_format

                    # Reshape the image so that it can be drawn on the VisPy canvas:
                    content.append(component.data.reshape(height, width))
                    timestamps.append(buffer.timestamp_ns)
            ia.stop_acquisition()

        if not return_xr:
            return np.array(content)

        if not HAS_XARRAY:
            raise ImportError('xarray should be installed for return_xr.')
        
        return xr.DataArray(
            np.array(content), dims=['time', 'x', 'y'], 
            coords={
                'time': ('time', (np.array(timestamps) - timestamps[0]) * 1e-9, {'unit': 'sec'}),
                'datetime': start_datetime
            }, attrs=self.get_current_configuration()
        )

    def __del__(self):
        self.h.reset()