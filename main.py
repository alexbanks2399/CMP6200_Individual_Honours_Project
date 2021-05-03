import csv
import datetime
import getpass
from netmiko import Netmiko
from jinja2 import Template

# Planned pseudo code
# Ask user for input files; device data, template file
# Generate config to apply
# Ask user for device credentials
# Apply generated config to given device


start_time = datetime.datetime.now()


def config_generator():
    generated_configs = ""
    device_ips = ""

    with open("switchport-interface-template.j2") as f:
        interface_template = Template(f.read(), keep_trailing_newline=True, autoescape=True)
    with open("switch_data.csv", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            generated_config = interface_template.render(
                device_name=row["Device Name"],
                date_time=datetime.datetime.now().isoformat(timespec='minutes'),
                interface=row["Interface"],
                connected=row["Connected to"],
                link=row["Link"],
                purpose=row["Purpose"],
                vlan=row["VLAN"]
            )
            device_name = row["Device Name"]
            device_ip = row["Device IP"]

            generated_configs += generated_config
            device_ips += device_ip + "\n"

    with open("configs.txt", "a") as f:
        f.write(generated_configs)
        print("Config file: ", f.name)
    with open("device_generated.txt", "a") as f:
        f.write(device_ips + "\n")
        print("Device list: ", f.name)


def config_applier():
    config = open("configs.txt")
    devicelist = []
    device = open("device_generated.txt")
    username = input("Input device username: ")
    password = getpass.getpass("Input device password: ")
    secret = getpass.getpass("Input device secret: ")

    for line in device:
        line = line.rstrip()
        devicelist.append(line)

    config_set = config

    for host in devicelist:
        net_connect = Netmiko(
            host,
            username=username,
            password=password,
            device_type="cisco_nxos",
            secret=secret)

        print(net_connect.find_prompt())
        print(net_connect.enable())

        output = net_connect.send_config_set(config_set)
        print(net_connect.send_config_set(config_set))
        print(net_connect.save_config())
        print(net_connect.disconnect())

        with open("audit.txt", "a") as f:
            f.write(output)

    print("See 'audit.txt' for confirmation of process")


config_generator()
config_applier()
