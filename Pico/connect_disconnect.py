#code will connect and disconnet from network

import network
import time
import urandom

# Initialize WiFi interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Target network details
TARGET_SSID = "type something"  # Replace with the target network SSID
TARGET_PASSWORD = "change me"  # Leave empty if the network is open

def simulate_deauth():
    print(f"Attempting to connect to {TARGET_SSID}")
    wlan.connect(TARGET_SSID, TARGET_PASSWORD)
    
    # Wait for connection or timeout
    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            print("Connected. Disconnecting...")
            wlan.disconnect()
            break
        max_wait -= 1
        time.sleep(1)
    
    if not wlan.isconnected():
        print("Failed to connect")
    
    time.sleep(1)  # Short delay before next attempt

print(f"Starting simulated deauth attack on {TARGET_SSID}")

try:
    while True:
        simulate_deauth()
except KeyboardInterrupt:
    print("Attack stopped by user")
finally:
    # Reset WiFi interface
    wlan.disconnect()
    wlan.active(False)
    print("WiFi interface reset")