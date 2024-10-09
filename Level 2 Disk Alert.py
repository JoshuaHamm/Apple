import re
import subprocess
from urllib.parse import quote

print("Initial Description: ")

user_input = ""
disk_free = ""
disk_usage = ""
total_disk = ""

while True:
    line = input()
    if "Disk Usage: " in line and "%" in line and any(char.isdigit() for char in line):
        disk_usage = line.split(":")[1].strip()
        disk_usage = disk_usage[:-2].strip()
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

        elif line.startswith("Total disk size:"):
            total_disk = line.split(":")[1].strip()
        elif line.startswith("Disk free space:"):
            disk_free = line.split(":")[1].strip()

while True:
    subject_line = input("Ticket Summary Line: ")
    if "Service Ticket #" not in subject_line:
        print("The input does not contain 'Service Ticket #'. Please try again.")
    else:
        break  # Exit the loop if the condition is met

while True:
    contact_email = input("Contact Email: ")
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, contact_email) is not None:
        break # Exit the loop if the condition is met
    else:
        print("Invalid Email Address. Please try again.")

while True:
    contact_fn = input("Contact First Name: ")
    if contact_fn is None:
        print("Contact First Name cannot be blank. Please try again.")
    else:
        break # Exit the loop if the condition is met
    
sender = ""
receivers = ["help@nexigen.com", contact_email]

print(disk_usage + "--------------------------")

def open_mail_client(sender, receiver, subject, body):
    mailto_link = f"mailto:{receiver}?subject={quote(subject)}&body={quote(body)}"
    subprocess.run(["open", mailto_link])

if __name__ == "__main__":
    email_sender = sender
    receiver = "; ".join(receivers)
    subject = subject_line
    body = f"""
        {contact_fn},

        We received an alert that {device_name} went into a {device_state} state for disk usage on disk C. At the time of the alert, the disk was {disk_usage}% full having {disk_free} free of {total_disk}.

        If this is something you would like Nexigen to investigate further billed as Time and Material, please let us know!
        """

    open_mail_client(sender, receiver, subject, body)
    print("Email client opened with the composed email.")