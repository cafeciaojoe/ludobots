# usb_config.py
import usb.core
import usb.backend.libusb1

def initialize_usb():
    conda_libusb = '/Users/joseph/opt/anaconda3/envs/ludo-drone/lib/libusb-1.0.dylib'
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: conda_libusb)
    if not backend:
        raise RuntimeError("Could not initialize USB backend")
    usb.core.find(backend=backend)  # Set globally

# Initialize when module is imported
initialize_usb()
