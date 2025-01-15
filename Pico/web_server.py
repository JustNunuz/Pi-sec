import network
import socket
import machine
import time

# Setup LED and Temperature Sensor
led = machine.Pin("LED", machine.Pin.OUT)  # Onboard LED control
sensor_temp = machine.ADC(4)  # Temperature sensor on Pico W
conversion_factor = 3.3 / (65535)

# Wi-Fi credentials
ssid = 'change me'
password = 'type something'

# Connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Connecting to WiFi...')
        time.sleep(10)

    print('Connected to WiFi')
    print(wlan.ifconfig())  # Print IP address

# Read temperature
def read_temperature():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721  # Pico W temperature calculation
    return temperature

# Create a webpage that controls the LED and shows temperature
def webpage(state, temperature):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Pico W Web Control</title></head>
        <body>
            <form action="/lighton">
                <input type="submit" value="Light on" />
            </form>
            <form action="/lightoff">
                <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature:.2f} °C</p>
        </body>
        </html>
    """
    return html

# Start a web server
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse the socket
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        request = str(request)
        print('Request:', request)

        # Control LED based on the request
        if '/lighton' in request:
            print('Turning LED on')
            led.value(1)

        if '/lightoff' in request:
            print('Turning LED off')
            led.value(0)

        # Get the current LED state and temperature
        led_state = 'on' if led.value() == 1 else 'off'
        temperature = read_temperature()

        # Serve the webpage
        response = webpage(led_state, temperature)
        cl.send('HTTP/1.1 200 OK\n')
        cl.send('Content-Type: text/html\n')
        cl.send('Connection: close\n\n')
        cl.sendall(response)
        cl.close()

# Main program
connect_to_wifi()
start_server()
