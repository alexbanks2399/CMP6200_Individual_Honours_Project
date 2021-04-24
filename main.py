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

source_file = "switch_data.csv"
interface_template_file = "switchport-interface-template.j2"


def config_generator():
    generated_configs = ""
    device_ips = ""

    with open(interface_template_file) as f:
        interface_template = Template(f.read(), keep_trailing_newline=True, autoescape=True)
    with open(source_file, encoding="utf-8-sig") as f:
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
    with open("device_list.txt", "a") as f:
        f.write(device_ips + "\n")
        print("Device list: ", f.name)


def config_applier():
    sites = open("device_list.txt")
    config = open("configs.txt")
    devicelist = []
    username = input("Input device username: ")
    password = getpass.getpass("Input device password: ")
    secret = getpass.getpass("Input device secret: ")

    for line in sites:
        line = line.rstrip()
        devicelist.append(line)

    config_set = config.split("\n")

    for host in devicelist:
        net_connect = Netmiko(
            host,
            username=username,
            password=password,
            device_type="cisco_ios",
            secret=secret)

        print(net_connect.find_prompt())
        net_connect.enable()

        output = net_connect.send_config_set(config_set)
        net_connect.save_config()
        print(net_connect.send_command("show int status"))
        net_connect.disconnect()

        with open("audit.txt", "a") as f:
            f.write(output)

        print("See 'audit.txt' for confirmation of process")


config_generator()
# config_applier()
