import usbtmc
import time


# number of comunication trial
NUM_COMUNICATE = 3

class PWR01:
    def __init__(self, venderID='0x0b3e', productID='0x1049'):
        usb_id = "USB::{}::{}::INSTR".format(venderID, productID)
        self._instr = None
        for _ in range(NUM_COMUNICATE):
            instr = usbtmc.Instrument("USB::0x0b3e::0x1049::INSTR")
            try:
                instr.ask("*IDN?")
                self._instr = instr
            except Exception:
                pass
        if self._instr is None:
            raise IOError('Instrument is not found in {}.'.format(usb_id))

    @property
    def is_on(self):
        return self._instr.ask("OUTP?") == '1'
    
    @property
    def is_off(self):
        return not self.is_on

    def output_on(self):
        if self.is_off:
            self._instr.write("OUTP ON")
    
    def output_off(self): 
        if self.is_on:
            self._instr.write("OUTP OFF")

    def set_current(self, value):
        """
        Set the constant current control
        """
        self._instr.write("CURR {}".format(value))

    def set_voltage(self, value):
        """
        Set the constant voltage control
        """
        self._instr.write("VOLT {}".format(value))
        
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