import csv
import datetime
import getpass
import netmiko
from jinja2 import Template

# Planned pseudo code
# Ask user for input files; device data, template file
# Generate config to apply
# Ask user for device credentials
# Apply generated config to given device

start_time = datetime.datetime.now()

generated_configs = ""
input_csv = input("Input file: ")

with open("switchport-interface-template.j2") as f:
    interface_template = Template(f.read(), keep_trailing_newline=True, autoescape=True)

with open(input_csv, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        generated_config = interface_template.render(
            interface=row["Interface"],
            connected=row["Connected to"],
            link=row["Link"],
            purpose=row["Purpose"],
            vlan=row["VLAN"]
        )

        generated_configs += generated_config

device = {"address": input("Device address: "),
          "device_type": "cisco_nxos",
          "username": input("Username: "),
          "password": getpass.getpass("Password: "),
          "secret": getpass.getpass("Secret: ")}

with open("configs.txt", "a") as f:
    f.write(generated_configs)
    print("Config output file: ", f.name)

config_set = generated_configs.split("\n")

with netmiko.ConnectHandler(ip=device["address"],
                            device_type=device["device_type"],
                            username=device["username"],
                            password=device["password"],
                            secret=device["secret"]) as connector:
    print("Connected to: ", connector.find_prompt())
    output = connector.send_config_set(config_set)
    print("Disconnecting...")
    connector.disconnect()
    print("Disconnected.")

with open("audit.txt", "a") as f:
    f.write(output)

print("See 'audit.txt' for accounting")
print("Time taken: ", datetime.datetime.now() - start_time)
