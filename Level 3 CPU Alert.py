import re
import subprocess

print("Original Ticket Notes: ")

user_input = ""
deviceName = None
date = None
time = None
cpu_usage = None
top_processes = [None] * 5
users = [None] * 5
cpu_usages = [None] * 5

while True:
    line = input()
    if "CPU Usage for Process 5:" in line and "%" in line and any(char.isdigit() for char in line):
        user_input += line + "\n"
        break
    user_input += line + "\n"

for line in user_input.split("\n"):
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
    elif line.startswith("CPU Usage:"):
        cpu_usage = line.split(":")[1].strip()
    elif line.startswith("Top Process"):
        process_index = int(line.split(":")[0].split()[-1]) - 1
        top_processes[process_index] = line.split(":")[1].strip()
    elif line.startswith("User of Process"):
        user_index = int(line.split(":")[0].split()[-1]) - 1
        users[user_index] = line.split(":")[1].strip()
    elif "CPU Usage for Process 5:" in line:
        match = re.search(r'\d+\.\d+', line)
        if match:
            cpu_usages[4] = match.group()
    elif line.startswith("CPU Usage for Process"):
        process_index = int(line.split(":")[0].split()[-1]) - 1
        match = re.search(r'\d+\.\d+', line)
        if match:
            cpu_usages[process_index] = match.group()

UserOfProcess1, UserOfProcess2, UserOfProcess3, UserOfProcess4, UserOfProcess5 = users
CPUUsageForProcess1, CPUUsageForProcess2, CPUUsageForProcess3, CPUUsageForProcess4, CPUUsageForProcess5 = cpu_usages

while True:
    subjectLine = input("Ticket Summary Line: ")
    if "Service Ticket #" not in subjectLine:
        print("The input does not contain 'Service Ticket #'. Please try again.")
    else:
        break  # Exit the loop if the condition is met
while True:
    currentState = input("Current CPU State (Normal, Warning or Failed): ")
    if "normal" not in currentState.lower() and "warning" not in currentState.lower() and "failed" not in currentState.lower():
        print("CPU State not Recognized. Please try again.")
    else:
        break  # Exit the loop if the condition is met
    
while True:
    service_team = input("Service Team: ")
    if not service_team:
        print("Service Team not entered. Please try again.")
    else:
        break  # Exit the loop if the condition is met



sender = ""
receivers = ["help@nexigen.com"]

def create_email(sender, receiver, subject, body):
    mailto_link = f"mailto:{receiver}?subject={subject}&body={body}"
    subprocess.run(["open", mailto_link])

if __name__ == "__main__":
    email_sender = sender
    receiver = "; ".join(receivers)
    subject = subjectLine
    body = f"""Attention Team {service_team} Engineer,

    We received an alert that server {deviceName} entered a {deviceState} state on {date} at {time}. Below is more information about the Alert.

    The device is currently in a {currentState} State.

    Total CPU Usage: {cpu_usage}

    Top Processes:
    {top_processes[0]} - {cpu_usages[0]}%
    {top_processes[1]} - {cpu_usages[1]}%
    {top_processes[2]} - {cpu_usages[2]}%
    {top_processes[3]} - {cpu_usages[3]}%
    {top_processes[4]} - {cpu_usages[4]}%

    Users of Top Processes:
    {top_processes[0]} - {UserOfProcess1}
    {top_processes[1]} - {UserOfProcess2}
    {top_processes[2]} - {UserOfProcess3}
    {top_processes[3]} - {UserOfProcess4}
    {top_processes[4]} - {UserOfProcess5}

    Attach screenshots of utilization and processes for further analysis.
    """

    create_email(sender, receiver, subject, body)