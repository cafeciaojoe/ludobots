import usb.core
import usb.backend.libusb1
import os
import sys

def debug_libusb():
    print(f"Python version: {sys.version}")
    print(f"PyUSB version: {usb.__version__}")

    paths = [
        '/opt/homebrew/lib/libusb-1.0.dylib',
        '/usr/local/lib/libusb-1.0.dylib',
        os.path.join(os.environ.get('CONDA_PREFIX', ''), 'lib', 'libusb-1.0.dylib')
    ]

    print("\nChecking libusb paths:")
    for path in paths:
        exists = os.path.exists(path)
        print(f"{path}: {'EXISTS' if exists else 'NOT FOUND'}")
        if exists:
            print(f"File permissions: {oct(os.stat(path).st_mode)[-3:]}")

    print("\nTrying to load backend:")
    for path in paths:
        if os.path.exists(path):
            try:
                print(f"\nAttempting to load: {path}")
                backend = usb.backend.libusb1.get_backend(find_library=lambda x: path)
                if backend:
                    print(f"Successfully loaded backend from: {path}")
                    return backend
                else:
                    print(f"Backend creation returned None for: {path}")
            except Exception as e:
                print(f"Error loading {path}: {str(e)}")

    return None

print("Starting USB backend test...")
backend = debug_libusb()

if backend:
    print("\nTrying to enumerate USB devices:")
    try:
        devices = list(usb.core.find(backend=backend, find_all=True))
        print(f"Found {len(devices)} USB devices")
        for dev in devices:
            print(f"Device ID {dev.idVendor:04x}:{dev.idProduct:04x}")
    except Exception as e:
        print(f"Error enumerating devices: {str(e)}")
else:
    print("\nFailed to initialize USB backend")
