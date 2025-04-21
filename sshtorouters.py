#!/usr/bin/env python3

import os
from netmiko import ConnectHandler
import json

def get_sshinfo():
    file = "SSHinfo.json"

    if not os.path.exists(file):
        print(f"Error: File '{file}' is not found")
        return None

    try:
        with open(file, "r") as f:
            data = json.load(f)
        return data

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{file}'. Details: {e}")
        return None

def ssh_into_routers(ssh_data):
    for router in ssh_data:
        device = {
            "device_type": "cisco_ios",
            "host": router["IP"],
            "username": router["username"],
            "password": router["password"],
        }

        try:
            print(f"Connecting to {router['hostname']} ({router['IP']})...")
            connection = ConnectHandler(**device)
            print(f"SSH to Routers Sucessfully")
            connection.disconnect()
        except Exception as e:
            print(f"Failed to connect to {router['hostname']} ({router['IP']}): {e}")

if __name__ == "__main__":
    ssh_data = get_sshinfo()
    if ssh_data:
        ssh_into_routers(ssh_data)
    else:
        print("Error loading SSH data")
