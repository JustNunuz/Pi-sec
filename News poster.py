import network
import urequests
import time

# Connect to Wi-Fi
ssid = 'change me'
password = 'type something'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # Wait for connection
    max_wait = 10  # seconds to wait for connection
    while max_wait > 0:
        if wlan.isconnected():
            print('Connected to Wi-Fi')
            print(wlan.ifconfig())  # Show IP info
            return True
        max_wait -= 1
        print("Waiting for Wi-Fi connection...")
        time.sleep(1)
    
    print("Failed to connect to Wi-Fi")
    return False

# Function to fetch HTML from Hacker News with error handling
def fetch_html(url):
    try:
        response = urequests.get(url)
        html = response.text
        response.close()
        return html
    except Exception as e:
        print(f"Failed to fetch HTML: {e}")
        return None

# Function to extract headlines based on the HTML snippet provided
def extract_headlines(html):
    if html is None:
        print("No HTML content to extract from.")
        return []
    
    headlines = []
    pos = 0
    while True:
        # Find the position of the <span class="titleline"> containing the link
        pos = html.find('<span class="titleline">', pos)
        if pos == -1:
            break

        # Extract the URL and Title
        start_url = html.find('<a href="', pos) + len('<a href="')
        end_url = html.find('"', start_url)
        start_title = html.find('>', start_url) + 1
        end_title = html.find('</a>', start_title)

        if start_url != -1 and end_url != -1 and start_title != -1 and end_title != -1:
            url = html[start_url:end_url]
            title = html[start_title:end_title]
            headlines.append((title, url))
        
        pos = end_title

    return headlines

# Main execution flow
if connect_wifi():
    # Fetch Hacker News headlines
    url = "https://news.ycombinator.com/"
    html = fetch_html(url)

    if html:
        # Extract and print one headline every 10 seconds
        headlines = extract_headlines(html)
        
        if not headlines:
            print("No headlines found.")
        else:
            for i, (title, url) in enumerate(headlines):
                print(f"{i + 1}. {title} ({url})")
                time.sleep(10)  # Wait for 10 seconds before printing the next headline
    else:
        print("Could not retrieve HTML.")
else:
    print("Wi-Fi connection failed. Check your credentials or signal strength.")
