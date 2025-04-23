#!/usr/bin/env python3

import os
import json
from netmiko import ConnectHandler

CONFIG_DIR = "."

# Load credentials from SSHinfo.json
with open("SSHinfo.json", "r") as file:
    json_data = json.load(file)
    ROUTER_CREDENTIALS = {
        entry["hostname"]: {
            "hostname": entry["IP"],
            "username": entry["username"],
            "password": entry["password"]
        }
        for entry in json_data
    }

def get_router_config(router_name, hostname, username, password):
    device = {
        "device_type": "cisco_ios",
        "ip": hostname,
        "username": username,
        "password": password,
        "port": 22,
        "verbose": False,
    }

    try:
        connection = ConnectHandler(**device)
        connection.enable()
        running_config = connection.send_command("show running-config")
        connection.disconnect()
        return running_config.splitlines()
    except Exception as e:
        print(f"Error fetching config for {router_name}: {e}")
        return None

def get_latest_saved_config(router_name):
    files = [f for f in os.listdir(CONFIG_DIR) if f.startswith(f"Router ({router_name})")]

    if not files:
        return None

    latest_file = sorted(files, reverse=True)[0]
    with open(os.path.join(CONFIG_DIR, latest_file), "r") as f:
        return f.read().splitlines()

def compare_configs(router_name, new_config):
    old_config = get_latest_saved_config(router_name)

    if old_config is None:
        return [f"No previous config found for {router_name}.\n"]

    ignore_keywords = [
        "Building configuration",
        "Current configuration",
        "Last configuration change",
        "hostname",
        "!",
        "end"
    ]

    def is_valid(line):
        return line.strip() != "" and all(k not in line for k in ignore_keywords)

    # Strip, filter, and convert to sets for unordered comparison
    old_clean = set(line.strip() for line in old_config if is_valid(line))
    new_clean = set(line.strip() for line in new_config if is_valid(line))

    added = new_clean - old_clean
    removed = old_clean - new_clean

    changes = []

    for line in sorted(removed):
        changes.append(f"OLD CONFIG: {line}\n")
    for line in sorted(added):
        changes.append(f"NEW CONFIG: {line}\n")

    return changes if changes else [f"No significant changes detected for {router_name}.\n"]

def main():
    results = {}

    for router, creds in ROUTER_CREDENTIALS.items():
        new_config = get_router_config(router, creds["hostname"], creds["username"], creds["password"])
        if new_config:
            changes = compare_configs(router, new_config)
            results[router] = changes
        else:
            results[router] = [f"Failed to fetch config for {router}"]

    return results
