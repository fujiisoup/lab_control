import platform
if platform.system() == 'Windows':
    from .usb1208LS_win import usb_1208LS
else:
    from .usb1208LS import usb_1208LS