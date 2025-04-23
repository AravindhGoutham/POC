#!/usr/bin/env python3

import json
from netmiko import ConnectHandler

# Load SSH credentials
with open("SSHinfo.json") as f:
    routers = json.load(f)

# SNMP configuration commands
snmp_config = [
    "snmp-server community private RW",
    "snmp-server host 198.51.100.2 version 2c private",
    "snmp-server enable traps"
]

for router in routers:
    hostname = router["hostname"]
    ip = router["IP"]
    username = router["username"]
    password = router["password"]

    print(f"\nConnecting to {hostname} ({ip})")

    try:
        conn = ConnectHandler(
            device_type="cisco_ios",
            host=ip,
            username=username,
            password=password
        )

        output = conn.send_config_set(snmp_config)
        print(f"Config pushed to {hostname}:\n{output}")

        save_output = conn.save_config()
        print(f"Configuration saved on {hostname}:\n{save_output}")

        conn.disconnect()

    except Exception as e:
        print(f"Failed to configure {hostname}: {e}")
