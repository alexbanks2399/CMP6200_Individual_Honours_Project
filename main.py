import csv
import datetime
import tkinter
from tkinter import *
from netmiko import Netmiko
from jinja2 import Template
import getpass

start_time = datetime.datetime.now()


# source_file = "switch_data.csv"
# interface_template_file = "switchport-interface-template.j2"


def file_browser():
    tkinter.askopenfilename(parent=tkinter,
                            initialdir="C:\My Documents\Documents",
                            title="Select a file",
                            filetypes=(("All files", "*.*"),
                                       ("Text files", "*.txt"),
                                       ("CSV files", "*.csv"),
                                       ("Jinja Templates", "*.j2"))
                            )
    tkinter.mainloop()


def config_generator():
    generated_configs = ""
    device_ips = ""

    with open(interface_template_file) as f:
        interface_template = Template(f.read(), keep_trailing_newline=True)
    with open(source_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            generated_config = interface_template.render(
                device_name=row["Device Name"],
                date_time=datetime.datetime.now().isoformat(timespec='minutes'),
                interface=row["Interface"],
                connected=row["Connected"],
                link=row["Link"],
                purpose=row["Purpose"],
                vlan=row["VLAN"]
            )
            device_name = row["Device Name"]
            device_ip = row["Device IP"]

            generated_configs += generated_config
            device_ips += device_ip + "\n"

    with open(device_name + "_config.txt", "a") as f:
        f.write(generated_configs)
    with open("device_list.txt", "a") as f:
        f.write(device_ips + "\n")


def config_applier():
    sites = open("device_list.txt")
    devicelist = []
    username = input("Input device username: ")
    password = getpass.getpass("Input device password: ")
    secret = getpass.getpass("Input device secret: ")

    for line in sites:
        line = line.rstrip()
        devicelist.append(line)

    for host in devicelist:
        net_connect = Netmiko(
            host,
            username=username,
            password=password,
            device_type="cisco_ios",
            secret=secret)


source_file = file_browser()
interface_template_file = file_browser()
config_generator()
# config_applier()
