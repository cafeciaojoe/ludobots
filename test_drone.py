# test_drone.py
import cflib.crtp

import usb_config  # This will set up the backend (from chatgpt) 

def test_drone_connection():
    cflib.crtp.init_drivers()
    available = cflib.crtp.scan_interfaces()
    print(f"Available interfaces: {available}")

if __name__ == '__main__':
    test_drone_connection()
