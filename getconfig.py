#!/usr/bin/env python3

from napalm import get_network_driver
import json
from datetime import datetime

def configurations():
    driver = get_network_driver("ios")

    with open("SSHinfo.json", "r") as f:
        ssh_info = json.load(f)
    routers = []
    for entry in ssh_info:
        routers.append({
            "hostname": entry["IP"],
            "Device": f"Router ({entry['hostname']})",
            "username": entry["username"],
            "password": entry["password"],
            "platform": "ios"
        })
    saved_files = []
    for router in routers:
        try:
            router_conn = driver(hostname=router["hostname"],
                                 username=router["username"],
                                 password=router["password"])
            router_conn.open()
            print(f"Connecting to {router['hostname']}")
            output = router_conn.get_config()["running"]
            router_conn.close()
            timestamp = datetime.utcnow().strftime('%Y-%m-%d T %H-%M-%S')
            filename = f"{router['Device']}:{timestamp}.txt"
            with open(filename, "w") as file:
                file.write(output)
            print(f"Config file is saved as: {filename}")
            saved_files.append(filename)
        except Exception as e:
            print(f"Failed to get config: {e}")
    return saved_files
if __name__ == "__main__":
    configurations()
