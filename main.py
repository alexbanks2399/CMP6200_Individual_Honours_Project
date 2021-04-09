import csv
import datetime
from jinja2 import Template

source_file = "switch_data.csv"
interface_template_file = "switchport-interface-template.j2"


def config_generator():
    generated_configs = ""

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
            generated_configs += generated_config

    with open(device_name + "_config.txt", "a") as f:
        f.write(generated_configs)


config_generator()
