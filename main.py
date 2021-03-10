import csv
from jinja2 import Template

source_file = "switch_data.csv"
interface_template_file = "switchport-interface-template.j2"

interface_configs = ""

with open(interface_template_file) as f:
    interface_template = Template(f.read(), keep_trailing_newline=True)

with open(source_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        interface_config = interface_template.render(
            interface=row["Interface"],
            connected=row["Connected"],
            link=row["Link"],
            purpose=row["Purpose"],
            vlan=row["VLAN"]
        )
        interface_configs += interface_config

with open("interface_configs.txt", "w") as f:
    f.write(interface_configs)
