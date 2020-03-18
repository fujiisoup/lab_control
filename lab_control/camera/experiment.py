from FLI import FLI
import numpy as np
import sys
sys.path.append('../')
from spectrometer import thr640
import time
import logging
import csv
import xarray as xr
import matplotlib.pyplot as plt

# logger
logger = thr640.logger

# global instance
fli = FLI()
wavelength_controller = thr640.THR640()

"""
一枚だけ撮影するときに使う
"""
def take_one_shoot(vbin,exposuretime,count,sleep):
    """
    Parameters
    ----------
    vbin : int
        縦のビニングサイズ

    exposuretime: int
        露光時間[ms]

    count : int
        分光器の回折格子の座標

    Returns
    -------
    
    """
    temperature = fli.getTemperature()
    # logger.info("カメラの温度: {}".format(fli.getTemperature()))
    fli.setExposureTime(exposuretime)
    fli.setVBin(vbin)
    fli.setImageArea(10,0,2058,512//vbin)
    time.sleep(.5)

    # start exposure
    fli.exposeFrame()
    time.sleep(sleep)

    # exposure終わったらgrab
    array = fli.grabFrame(out=np.empty((512//vbin,2048), np.uint16))
    data = xr.DataArray(array, dims=['y', 'x'], coords={'vbin': vbin}, 
                    attrs={'temperature': temperature,
                            'exposure_time': exposuretime,
                            'spectrometer_count': count
                            })
    return data

"""
撮影して回折格子動かす
"""
def move_and_shoot(count,exposure_time):
    wavelength_controller.goto(count=count)
    wavelength_controller.waitUntilReady()

    # start exposure
    fli.exposeFrame()
    # exposure終わったらgrab
    array = fli.grabFrame()
    time.sleep(.5)

    data = xr.DataArray(array, dims=['y', 'x'], coords={'spectrometer_count': count}, 
                        attrs={'temperature': fli.getTemperature(),
                               'device_status': fli.getDeviceStatus(),
                               'camera_mode': fli.getCameraModeString(0),
                               'exposure_time': exposure_time
                               })
    return data

"""
撮影して回折格子動かす(早いver)
"""
def fast_move_and_shoot(count,exposure_time):
    wavelength_controller.goto(count=count)

    # start exposure
    fli.exposeFrame()
    # exposure終わったらgrab
    array = fli.grabFrame()
    time.sleep(.5)

    data = xr.DataArray(array, dims=['y', 'x'], coords={'spectrometer_count': count}, 
                        attrs={'temperature': fli.getTemperature(),
                               'device_status': fli.getDeviceStatus(),
                               'camera_mode': fli.getCameraModeString(0),
                               'exposure_time': exposure_time
                               })
    return data

"""
撮影して回折格子動かすを繰り返す
"""
def repeat_move_and_shoot(start_count,count_interval,taken_count,exposuretime,output_dir):
    fli.setExposureTime(exposuretime)

    for i in range(taken_count):
        data = move_and_shoot(count=start_count,exposure_time=exposuretime)
        file=r'\output'+ str(i)+'.nc'
        data.to_netcdf(output_dir + file)
        start_count+=count_interval

"""
シャッターを開けて撮影、閉じて撮影して回折格子動かすを繰り返す
"""
def repeat_move_and_shoot_with_shutter_control(start_count,count_interval,taken_count,exposuretime,output_dir,output_dir_with_shutter_close):
    fli.setExposureTime(exposuretime)
    for i in range(taken_count):
        # -------shutterを開けて撮影---------
        fli.setFrameType('normal')
        time.sleep(1)
        # move
        wavelength_controller.goto(count=start_count)
        time.sleep(3)
        # start exposure
        fli.exposeFrame()
        array = fli.grabFrame()
        time.sleep(1)

        data = xr.DataArray(array, dims=['y', 'x'], coords={'spectrometer_count': start_count}, 
                            attrs={'temperature': fli.getTemperature(),
                                'device_status': fli.getDeviceStatus(),
                                'exposure_time': exposuretime,
                                'frame_type': 'normal'
                                })
        file=r'\output'+ str(i)+'.nc'
        data.to_netcdf(output_dir + file)

        time.sleep(3)

        # -------shutterを閉じて撮影---------
        fli.setFrameType('dark')
        time.sleep(1)

        fli.exposeFrame()
        array = fli.grabFrame()
        time.sleep(1)

        data = xr.DataArray(array, dims=['y', 'x'], coords={'spectrometer_count': start_count}, 
                            attrs={'temperature': fli.getTemperature(),
                                'device_status': fli.getDeviceStatus(),
                                'exposure_time': exposuretime,
                                'frame_type': 'dark'
                                })
        file=r'\output'+ str(i)+'_with_shutter_close'+'.nc'
        data.to_netcdf(output_dir_with_shutter_close + file)

        ## start_countあげて次のループへ
        start_count+=count_interval
        time.sleep(.5)


## exposuretime 動かしながら撮影、bin,tempreture固定
def shoot_and_update_exposure():
    output_dir = r'C:\Users\Public\Documents\seminar\exposuretime'

    ## 10ms~10e4msまで調べたい
    bitween = 0.1
    start = 0.9
    for i in range(31):
        start += bitween
        fli.setExposureTime(int(10**start))
        time.sleep(1)

        # start exposure
        fli.exposeFrame()
        # exposure終わったらgrab
        array = fli.grabFrame()
        time.sleep(.1)
        data = xr.DataArray(array, dims=['y', 'x'], coords={'exposure_time': int(10**start)}, 
                            attrs={'temperature': fli.getTemperature(),
                                'device_status': fli.getDeviceStatus(),
                                'camera_mode': fli.getCameraModeString(0)
                                })
        file=r'\output'+ str(i)+'.nc'
        data.to_netcdf(output_dir + file)
        print(str(i) +'done')
        time.sleep(2)


if __name__ == "__main__":
    print(fli.getTemperature())


