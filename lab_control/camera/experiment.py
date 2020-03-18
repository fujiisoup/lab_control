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

def take_one_shoot(vbin,exposuretime,count):
    """
    コントローラを動かさず1枚撮影

    Parameters
    ----------
    vbin : int
        縦のビニングサイズ

    exposuretime: int
        露光時間[ms]

    count : int
        分光器の回折格子の現在の座標

    Returns
    -------
    data: xr.DataArray
        撮影画像一枚
    """
    temperature = fli.getTemperature()　#xr.dataarrayのattrsに入れるのに必要

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


def move_and_shoot(vbin,count,exposuretime):
    """
    回折格子動かして撮影

    Parameters
    ----------
    vbin : int
        縦のビニングサイズ

    exposuretime: int
        露光時間[ms]

    count : int
        分光器の回折格子の移動後の座標

    Returns
    -------
    data: xr.DataArray
        撮影画像一枚
    """

    # 移動
    wavelength_controller.goto(count=count)
    wavelength_controller.waitUntilReady()
    data = take_one_shoot(count=count,exposuretime=exposuretime,vbin= vbin)
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
        
if __name__ == "__main__":
    # コントローラに表示されている座標123456においてビニングサイズ4　露光時間1秒で撮影したい場合
    move_and_shoot(vbin=4,exposuretime=1000,count=123456)



