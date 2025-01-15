import paramiko
import os
from dotenv import load_dotenv

command = "whoami"

# Update the next three lines with your
# Load environment variables from a .env file
load_dotenv()

# server's information
host = os.getenv("SSH_HOST")
username = os.getenv("SSH_USERNAME")
password = os.getenv("SSH_PASSWORD")

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
_stdin, _stdout,_stderr = client.exec_command("whoami")
print(_stdout.read().decode())
client.close()