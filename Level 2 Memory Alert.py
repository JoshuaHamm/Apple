import subprocess
import re
from urllib.parse import quote

print("Enter the initial description: ")

userInput = ""
physicalMemory = ""
virtualMemory = ""
physicalMemoryTop = [None] * 5
virtualMemoryTop = [None] * 5
topProcesses = [None] * 5

date = None
time = None

while True:
    line = input()
    if "Virtual Memory for Process 5:" in line and ("MB" in line or "GB" in line) and any(char.isdigit() for char in line):
        userInput += line + "\n"
        break
    userInput += line + "\n"

for line in userInput.split("\n"):
    if line.startswith("Device:"):
        deviceName = line.split(":")[1].strip()
    elif line.startswith("Issue:"):
        datetime_str = line.split("At ")[1].split(" the")[0]
        date_str, time_str = datetime_str.split(" ")
        date_parts = date_str.split("-")
        date = "{}/{}/{}".format(date_parts[1], date_parts[2], date_parts[0])
        hour, minute, second = time_str.split(":")
        hour = int(hour)
        if hour >= 12:
            time = "{}:{} PM".format(hour if hour == 12 else hour - 12, minute)
        else:
            time = "{}:{} AM".format(hour if hour > 0 else 12, minute)
        words = line.split()
        deviceState = words[-2]

    elif line.startswith("Physical Memory Usage:"):
        physicalMemory = line.split(":")[1].strip()

    elif line.startswith("Virtual Memory Usage:"):
        virtualMemory = line.split(":")[1].strip()

    elif line.startswith("Top Process"):
        process_index = int(line.split(":")[0].split()[-1]) - 1
        topProcesses[process_index] = line.split(":")[1].strip()

    #Generates list of physical memory for each process
    elif "Physical Memory for Process 5:" in line:
        match = re.search(r'(\d+\.\d+)\s*(MB|GB)', line)
        if match:
            physicalMemoryTop[4] = match.group()
    elif line.startswith("Physical Memory for Process"):
        process_index = int(line.split(":")[0].split()[-1]) - 1
        match = re.search(r'(\d+\.\d+)\s*(MB|GB)', line)
        if match:
            physicalMemoryTop[process_index] = match.group()

    #Generates list of virtual memory for each process
    elif "Virtual Memory for Process 5:" in line:
        match = re.search(r'(\d+\.\d+)\s*(MB|GB)', line)
        if match:
            virtualMemoryTop[4] = match.group()
    elif line.startswith("Virtual Memory for Process"):
        process_index = int(line.split(":")[0].split()[-1]) - 1
        match = re.search(r'(\d+\.\d+)\s*(MB|GB)', line)
        if match:
            virtualMemoryTop[process_index] = match.group()

while True:
    subjectLine = input("Ticket Summary Line: ")
    if "Service Ticket #" not in subjectLine:
        print("The input does not contain 'Service Ticket #'. Please try again.")
    else:
        break  # Exit the loop if the condition is met

while True:
    contactEmail = input("Contact Email: ")
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, contactEmail) is not None:
        break # Exit the loop if the condition is met
    else:
        print("Invalid Email Address. Please try again.")

while True:
    contactFN = input("Contact First Name: ")
    if contactFN is None:
        print("Contact First Name cannot be blank. Please try again.")
    else:
        break # Exit the loop if the condition is met
    
sender = ""
receivers = ["help@nexigen.com", contactEmail]

def open_mail_client(sender, receiver, subject, body):
    mailto_link = f"mailto:{receiver}?subject={quote(subject)}&body={quote(body)}"
    subprocess.run(["open", mailto_link])

if __name__ == "__main__":
    email_sender = sender
    receiver = "; ".join(receivers)
    subject = subjectLine
    body = f"""
{contactFN},
 
We received an alert that {deviceName} went into a {deviceState} state for memory utilization on {date} at {time}. Below is more information about the alert when it was generated.
 
Physical Memory Usage: {physicalMemory}%
Virtual Memory Usage: {virtualMemory}%
 
Top Process by Physical Memory Usage
{topProcesses[0]} - {physicalMemoryTop[0]}
{topProcesses[1]} - {physicalMemoryTop[1]}
{topProcesses[2]} - {physicalMemoryTop[2]}
{topProcesses[3]} - {physicalMemoryTop[3]}
{topProcesses[4]} - {physicalMemoryTop[4]}
 
Top Process by Virtual Memory Usage
{topProcesses[0]} - {virtualMemoryTop[0]}
{topProcesses[1]} - {virtualMemoryTop[1]}
{topProcesses[2]} - {virtualMemoryTop[2]}
{topProcesses[3]} - {virtualMemoryTop[3]}
{topProcesses[4]} - {virtualMemoryTop[4]}
 
If this is something you would like Nexigen to investigate further, or if you have any questions about the alert, please let us know!
        """

    open_mail_client(sender, receiver, subject, body)
    print("Email client opened with the composed email.")
