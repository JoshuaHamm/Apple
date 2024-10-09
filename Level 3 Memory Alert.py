import subprocess
import re
from urllib.parse import quote

print("Enter the initial description: ")

team_name = ""
user_input = ""
physical_memory = ""
virtual_memory = ""
physical_memory_top = [None] * 5
virtual_memory_top = [None] * 5
top_processes = [None] * 5

date = None
time = None

while True:
    line = input()
    if "Virtual Memory for Process 5:" in line and ("MB" in line or "GB" in line) and any(char.isdigit() for char in line):
        user_input += line + "\n"
        break
    user_input += line + "\n"

for line in user_input.split("\n"):
    if line.startswith("Device:"):
        device_name = line.split(":")[1].strip()
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
        device_state = words[-2]

    elif line.startswith("Physical Memory Usage:"):
        physical_memory = line.split(":")[1].strip()

    elif line.startswith("Virtual Memory Usage:"):
        virtual_memory = line.split(":")[1].strip()

    elif line.startswith("Top Process"):
        process_index = int(line.split(":")[0].split()[-1]) - 1
        top_processes[process_index] = line.split(":")[1].strip()

    # Generates list of physical memory for each process
    elif "Physical Memory for Process 5:" in line:
        match = re.search(r'(\d+\.\d+)\s*(MB|GB)', line)
        if match:
            physical_memory_top[4] = match.group()
    elif line.startswith("Physical Memory for Process"):
        process_index = int(line.split(":")[0].split()[-1]) - 1
        match = re.search(r'(\d+\.\d+)\s*(MB|GB)', line)
        if match:
            physical_memory_top[process_index] = match.group()

    # Generates list of virtual memory for each process
    elif "Virtual Memory for Process 5:" in line:
        match = re.search(r'(\d+\.\d+)\s*(MB|GB)', line)
        if match:
            virtual_memory_top[4] = match.group()
    elif line.startswith("Virtual Memory for Process"):
        process_index = int(line.split(":")[0].split()[-1]) - 1
        match = re.search(r'(\d+\.\d+)\s*(MB|GB)', line)
        if match:
            virtual_memory_top[process_index] = match.group()

while True:
    subject_line = input("Ticket Summary Line: ")
    if "Service Ticket #" not in subject_line:
        print("The input does not contain 'Service Ticket #'. Please try again.")
    else:
        break  # Exit the loop if the condition is met

while True:
    service_team = input("Service Team: ")
    if service_team != '1' and service_team != '2':
        print("Service Team not Recognized. Please try again.")
    else:
        break  # Exit the loop if the condition is met
 
while True:
    current_state = input("Current Memory State (Normal, Warning or Failed): ")
    if "normal" not in current_state.lower() and "warning" not in current_state.lower() and "failed" not in current_state.lower():
        print("Memory State not Recognized. Please try again.")
    else:
        break  # Exit the loop if the condition is met
   
sender = ""
receivers = ["help@nexigen.com"]

def open_mail_client(sender, receiver, subject, body):
    mailto_link = f"mailto:{receiver}?subject={quote(subject)}&body={quote(body)}"
    subprocess.run(["open", mailto_link])

if __name__ == "__main__":
    email_sender = sender
    receiver = "; ".join(receivers)
    subject = subject_line
    body = f"""
Attention Team {team_name} Engineer,
 
We received an alert that {device_name} went into a {device_state} state for memory utilization on {date} at {time}. Below is more information about the alert when it was generated.
{device_name} is currently in a {current_state} state for memory.

Physical Memory Usage: {physical_memory}%
Virtual Memory Usage: {virtual_memory}%
 
Top Process by Physical Memory Usage
{top_processes[0]} - {physical_memory_top[0]}
{top_processes[1]} - {physical_memory_top[1]}
{top_processes[2]} - {physical_memory_top[2]}
{top_processes[3]} - {physical_memory_top[3]}
{top_processes[4]} - {physical_memory_top[4]}
 
Top Process by Virtual Memory Usage
{top_processes[0]} - {virtual_memory_top[0]}
{top_processes[1]} - {virtual_memory_top[1]}
{top_processes[2]} - {virtual_memory_top[2]}
{top_processes[3]} - {virtual_memory_top[3]}
{top_processes[4]} - {virtual_memory_top[4]}
 
        """

    open_mail_client(sender, receiver, subject, body)
    print("Email client opened with the composed email.")
