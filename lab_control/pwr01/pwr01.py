import usbtmc
import usb.core
import time


# number of comunication trial
NUM_COMUNICATE = 3


class PWR01:
    def __init__(self, vendorID="0x0b3e", productID="0x1049"):
        usb_id = "USB::{}::{}::INSTR".format(vendorID, productID)
        self._instr = None
        for _ in range(NUM_COMUNICATE):
            try:
                instr = usbtmc.Instrument(
                    "USB::{}::{}::INSTR".format(vendorID, productID)
                )
            except usb.core.USBError:
                instr = usbtmc.Instrument(
                    usb.core.find(
                        idVendor=int(vendorID, 16), idProduct=int(productID, 16)
                    )
                )
                print(instr)
            try:
                instr.ask("*IDN?")
                self._instr = instr
            except Exception as e:
                print(e)
                pass
        if self._instr is None:
            raise IOError("Instrument is not found in {}.".format(usb_id))

    @property
    def is_on(self):
        return self._instr.ask("OUTP?") == "1"

    @property
    def is_off(self):
        return not self.is_on

    def output_on(self, max_time=None):
        """
        Turn the voltage / current on.
        If max_time is not None, wait until it is actually on
        """
        if self.is_off:
            self._instr.write("OUTP ON")

        if max_time is None:
            return

        start = time.time()
        while self.is_off:
            time.sleep(0.2)
            if time.time() > start + max_time:
                raise IOError("Cannot turn on.")

    def output_off(self, max_time=None):
        """
        Turn the voltage / current off.
        If max_time is not None, wait until it is actually off
        """
        if self.is_on:
            self._instr.write("OUTP OFF")

        if max_time is None:
            return

        start = time.time()
        while self.is_on:
            time.sleep(0.2)
            if time.time() > start + max_time:
                raise IOError("Cannot turn on.")

    def set_current(self, value):
        """
        Set the constant current control
        """
        self._instr.write("CURR:IMMediate {}".format(value))

    def get_current(self):
        """ Queries the measured value of the current.
        """
        return float(self._instr.ask("MEAS:CURR?"))

    def set_voltage(self, value):
        """
        Set the constant voltage control
        """
        self._instr.write("VOLT:IMM {}".format(value))

    def get_voltage(self):
        """ Queries the measured value of the voltage.
        """
        return float(self._instr.ask("MEAS:VOLT?"))

    def __del__(self):
        if self._instr is not None:
            self._instr.close()

    def reset(self):
        """
        Resets the panel settings.
        Clears alarms (if they cannot be cleared, alarms continue).
        Aborts the trigger subsystem operation.
        Clears the OPC bit (bit 0) of the status event register
        """
        self._instr.write("*RST")
