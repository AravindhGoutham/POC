#!/usr/bin/env python3

from napalm import get_network_driver
import json
from datetime import datetime

def configurations():
    driver = get_network_driver("ios")

    routers = [{"hostname": "198.51.100.1","Device":"Router (R1)", "username": "admin", "password": "admin", "platform": "ios"},
               {"hostname": "198.51.100.3","Device":"Router (R2)", "username": "admin", "password": "admin", "platform": "ios"},
               {"hostname": "198.51.100.4","Device":"Router (R3)", "username": "admin", "password": "admin", "platform": "ios"},
               {"hostname": "198.51.100.5","Device":"Router (R4)","username": "admin", "password": "admin", "platform": "ios"}]

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
            filename = f"{router['hostname']}:{timestamp}.txt"

            with open(filename, "w") as file:
                file.write(output)

            print(f"Config file is saved as: {filename}")
            saved_files.append(filename)

        except Exception as e:
            print(f"Failed to get config: {e}")

    return saved_files

if __name__ == "__main__":
    configurations()
