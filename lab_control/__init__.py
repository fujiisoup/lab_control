try:
    from . import wavemeter
except ImportError:
    pass

try:
    from .usb_1208LS import usb_1208LS
except ImportError:
    pass

try:
    from .pwr01 import pwr01
except ImportError:
    pass

try:  # they required pyserial only
    from .gsc01 import GSC01
    from . import sus
except ImportError:
    pass

from . import hamamatsu