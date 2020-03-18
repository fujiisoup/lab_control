import pyfli
import time 
class FLI: 
    def __init__(self):
        self.DEVICE = 'camera'
        self.INTERFACE = 'usb'
        self.FRAME_TYPE = "normal" # {'normal', 'dark', 'flood', 'flush'}
        
        fli_list = pyfli.FLIList(self.INTERFACE,self.DEVICE)

        if not fli_list:
            Exception("No device can be found")
        
        DEVICE_PATH, DEVICE_NAME = fli_list[0]
        self.handle = self.FLIOpen(DEVICE_PATH,self.INTERFACE,self.DEVICE)

    # mode: {0,1}, return value = xxkHZ
    def getCameraModeString(self,mode: int):
        return pyfli.getCameraModeString(self.handle,mode)

    # Get the remaining camera exposure time. exposure time given in milliseconds
    def getExposureStatus(self):
        return pyfli.getExposureStatus(self.handle)

    def getDeviceStatus(self):
        return pyfli.getDeviceStatus(self.handle)

    def getTemperature(self):
        return pyfli.getTemperature(self.handle)

    def grabFrame(self,out=None):
        """
        Grab frame.
        The size of the returned array is obtained from a call to `getReadoutDimensions`.

        Parameters
        ----------
        out : ndarray, optional
            The frame will be read into the `out` array if it is specified. It
            must have the correct dimensions to contain the frame, but it can
            have a different type than specified by `depth`.

        Returns
        -------
        frame : ndarray
            A 2-D ndarray. If `out` is given it will be a reference to `out`,
            otherwise it is a new array of type np.uint8 or np.uint16 depending
            on the value of `depth`.
        """

        return pyfli.grabFrame(self.handle, out=out)
    
    def getReadoutDimensions(self):
        """
        Get readout dimensions.
        Undocumented.

        Parameters
        ----------

        Returns
        -------
        width, hoffset, hbin, height, voffset, vbin: int
        
        Horizontal width and vertical height are in bins, hbin and vbin are the
        horizontal and vertical bin sizes respectively, and hoffset and
        voffset are the x-coordinate and y-coordinates of the upper left
        corner of the image area.
        """
        return pyfli.getReadoutDimensions(self.handle)

    def getArrayArea(self):
        """

        Get the array area of the given camera.

        This function finds the total area of the CCD array for camera dev.
        This area is specified in terms of a upper left point and a
        lower right point. The upper left x-coordinate is placed in ul x,
        the upper left y-coordinate is placed in ul y, the lower right
        x-coordinate is placed in lr x, and the lower right y-coordinate is
        placed in lr y.

        Parameters
        ----------
        dev : int
            Device handle.

        Returns
        -------
        ul_x, ul_y, lr_x, lr_y : int
            The coordinates of the upper left and lower right pixels.

        """
        return pyfli.getArrayArea(self.handle)

    def setFrameType(self,ftype):
        """
        Parameters
        ----------
        dev : int
            Device handle.

        ftype : {'normal', 'dark', 'flood', 'flush'}
            The frame type. The last two are associated with the RBI and
            are guesses as they aren't documented.
            I guess 'dark' type is taking photo without opening shutter.
        """
        pyfli.setFrameType(self.handle,ftype)

    def setHBin(self, hbin):
        """
        Parameters
        ----------
        hbin : int
            Bin horizontal dimension in pixels. The valid range is 1..16.
        """
        pyfli.setHBin(self.handle,hbin)


    def setVBin(self, vbin):
        """
        Parameters
        ----------
        vbin : int
            Bin vertical dimension in pixels. The valid range is 1..16.
        """
        pyfli.setVBin(self.handle,vbin)

    def setImageArea(self, ul_x, ul_y, lr_x, lr_y):
        """
        Set the image area of the camera.
        左上の座標(ul_x, ul_y)と右下の座標(lr_x, lr_y)が引数

        This function sets the image area to an area specified in terms of 
        a upper left point and a lower right point.
        The upper-left x-coordinate is `ul_x`, the upper left y-coordinate is
        `ul_y`, the lower right x-coordinate is `lr_x`, and the lower right
        y-coordinate is `lr_y`. Note that the given lower right coordinate
        must take into account the horizontal and vertical bin factor
        settings, but the upper left coordinate is absolute. In other
        words, the lower right coordinate used to set the image area is a
        virtual point (lr_x, lr_y) determined by:

            lr_x = ul_x + (lr_x' − ul_x)/hbin
            lr_y = ul_y + (lr_y' − ul_y)/vbin

        Where (lr_x, lr_y ) are the coordinates to pass to the
        FLISetImageArea function while (ul_x, ul_y) and (lr_x', lr_y') are
        the absolute coordinates of the desired image area, hbin is the
        horizontal bin factor, and vbin is the vertical bin factor.

        Note that the vertical and horizontal bins must be set separately.

        Parameters
        ----------
        dev : int
            Device handle.

        ul_x, ul_y, lr_x, lr_y : int
            The coordinates of the upper left and lower right pixels.
        """
        pyfli.setImageArea(self.handle, ul_x, ul_y, lr_x, lr_y)


    def exposeFrame(self):
        """
        Expose a frame for a given camera.

        This function exposes a frame according to the settings (image area,
        exposure time, bit depth, etc.) of the camera. The settings must be
        valid for the camera and are set by calling the appropriate functions.
        This function returns after the exposure has started.
        """
        pyfli.exposeFrame(self.handle)

    def cancelExposure(self):
        pyfli.cancelExposure(self.handle)

    # you should give exposure time in milliseconds
    def setExposureTime(self,time):
        pyfli.setExposureTime(self.handle,time)

    def setTemperature(self,t):
        pyfli.setTemperature(self.handle,t)

    def FLIOpen(self,device_path,interface,device):
        """
        Parameters
        ----------
        path : str
            Path to the device. The name of the device can be obtained from a
            call to FLIList. For parallel port devices that are not probed by
            FLIList (Windows 95/98/Me), place the address of the parallel port
            in a string in ascii form ie: "0x378". On Linux the device name
            will be something like ``/dev/xxx``

        interface : {'parallel-port', 'usb', 'serial', 'inet'}
            Interface type. The 'inet' type looks to be unsupported
            in libfli-1.104 and will raise an error.

        device : {'camera', 'filterwheel', 'focuser'}
            Device type.

        Returns
        -------
        handle : int
            Handle with which to call device functions.
        """
        return pyfli.FLIOpen(device_path,interface,device)

    def FLIClose(self):
        pyfli.FLIClose(self.handle)

    def unlockDevice(self):
        pyfli.unlockDevice(self.handle)
