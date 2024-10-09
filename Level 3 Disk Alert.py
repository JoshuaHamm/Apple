import subprocess
from urllib.parse import quote

print("Initial Description: ")

user_input = ""

disk_free = ""
disk_usage = ""
total_disk = ""
customer = ""

while True:
    line = input()
    if "Disk Usage: " in line and "%" in line and any(char.isdigit() for char in line):
        disk_usage = line.split(":")[1].strip()
        disk_usage = disk_usage[:-2].strip()
        user_input += line + "\n"
        break
    user_input += line + "\n"

device_name = ""
device_state = ""
date = ""
time = ""

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

    elif line.startswith("Total disk size:"):
        total_disk = line.split(":")[1].strip()
    elif line.startswith("Disk free space:"):
        disk_free = line.split(":")[1].strip()
    elif line.startswith("Customer:"):
        customer = line.split(":")[1].strip()

while True:
    subject_line = input("Ticket Summary Line: ")
    if "Service Ticket #" not in subject_line:
        print("The input does not contain 'Service Ticket #'. Please try again.")
    else:
        break  # Exit the loop if the condition is met

while True:
    service_team = input("Service Team: ")
    if service_team == "1" or service_team == "2":
        break
    else:
        print("Please enter a valid service team.")

# Prepare the email content
subject = subject_line
body = f"""Attention Team {service_team} Engineer,
Device is still in {device_state} state after remediation was ran. Please investigate the disk usage and take necessary actions.

Customer: {customer}
Device: {device_name}
(Insert screenshot of asset facts here)

Issue Date: {date}
Issue Time: {time}
Device State: {device_state}
Total Disk Size: {total_disk}
Disk Free Space: {disk_free}

Disk Usage: {disk_usage}%
(Insert Screenshot of Disk Usage here)


"""
# Encode the subject and body for the mailto URL
subject_encoded = quote(subject)
body_encoded = quote(body)

# Create the mailto URL
mailto_url = f"mailto:help@nexigen.com?subject={subject_encoded}&body={body_encoded}"

# Open the default mail client with the mailto URL
subprocess.run(["open", mailto_url])

