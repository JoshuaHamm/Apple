import re
import subprocess


print("Enter the initial description: ")

user_input = ""
device_name = None
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

user_of_process_1, user_of_process_2, user_of_process_3, user_of_process_4, user_of_process_5 = users
cpu_usage_for_process_1, cpu_usage_for_process_2, cpu_usage_for_process_3, cpu_usage_for_process_4, cpu_usage_for_process_5 = cpu_usages

while True:
    subject_line = input("Enter the Ticket Summary Line: ")
    if "Service Ticket #" not in subject_line:
        print("The input does not contain 'Service Ticket #'. Please try again.")
    else:
        break  # Exit the loop if the condition is met

receivers = ["romanfursenko@michelman.com", "TeresaHemmingway@michelman.com", "timkrebs@michelman.com", "tombolenbaugh@michelman.com"]
cc_recipients = ["help@nexigen.com", "jkiesewetter@nexigen.com", "ndutle@nexigen.com"]

def create_email(subject, body, receivers, cc_recipients):
    to_addresses = ", ".join(receivers)
    cc_addresses = ", ".join(cc_recipients)
    mailto_link = f"mailto:{to_addresses}?cc={cc_addresses}&subject={subject}&body={body}"
    subprocess.run(["open", mailto_link])

if __name__ == "__main__":
    subject = subject_line
    body = f"""Michelman Networking Team —

        We received an alert that server {device_name} entered a failed state on {date} at {time}. Below is more information regarding the Alert.

        Total CPU Usage: {cpu_usage}

        Top Processes:
        {top_processes[0]} - {cpu_usages[0]}%
        {top_processes[1]} - {cpu_usages[1]}%
        {top_processes[2]} - {cpu_usages[2]}%
        {top_processes[3]} - {cpu_usages[3]}%
        {top_processes[4]} - {cpu_usages[4]}%

        Users of Top Processes:
        {top_processes[0]} - {user_of_process_1} 
        {top_processes[1]} - {user_of_process_2}
        {top_processes[2]} - {user_of_process_3}
        {top_processes[3]} - {user_of_process_4}
        {top_processes[4]} - {user_of_process_5}

        If you have any issues or questions, or if you would like us to investigate the issue further, please let us know!
        """
    
    create_email(subject, body, receivers, cc_recipients)
    print("Email creation process initiated.")