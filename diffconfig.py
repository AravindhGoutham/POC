#!/usr/bin/env python3

import os
import napalm

CONFIG_DIR = "."
# This line defines a variable CONFIG_DIR and sets it to ".", which represents the current directory. This is where the script will look for saved configuration files.
ROUTER_CREDENTIALS = {
    "R1": {"hostname": "198.51.100.10", "username": "team", "password": "team"},
    "R2": {"hostname": "198.51.100.20", "username": "team", "password": "team"},
    "R3": {"hostname": "198.51.100.30", "username": "team", "password": "team"},
    "R4": {"hostname": "198.51.100.40", "username": "team", "password": "team"},
    "R5": {"hostname": "198.51.100.50", "username": "team", "password": "team"},
    "R6": {"hostname": "198.51.100.60", "username": "team", "password": "team"},
    "R7": {"hostname": "198.51.100.70", "username": "team", "password": "team"},
    "R8": {"hostname": "198.51.100.80", "username": "team", "password": "team"}
}

def get_router_config(router_name, hostname, username, password):
    driver = napalm.get_network_driver("ios")
    device = driver(hostname=hostname, username=username, password=password)

    try:
        device.open()  # opens the connection
        running_config = device.get_config()["running"]  # gets the running config when the connection is open
        device.close()  # the connection is closed
        return running_config.splitlines()  # Convert to list of lines for comparison
    except Exception as e:
        print(f"Error fetching config for {router_name}: {e}")
        return None

def get_latest_saved_config(router_name):
    files = [f for f in os.listdir(CONFIG_DIR) if f.startswith(f"Router ({router_name})")]

    if not files:
        return None

    latest_file = sorted(files, reverse=True)[0]  # sorts the list of files in reverse order so that we can get the latest file
    with open(os.path.join(CONFIG_DIR, latest_file), "r") as f:
        return f.read().splitlines()

def compare_configs(router_name, new_config):
    old_config = get_latest_saved_config(router_name)

    if old_config is None:
        return [f"No previous config found for {router_name}.\n"]

    changes = []

    for old, new in zip(old_config, new_config):  # compares each line of the old and new configs
        if old != new:
            changes.append(f"OLD CONFIG: {old}\nNEW CONFIG: {new}\n")

    for new in new_config:  # checks for lines in the new config that don't exist in the old config
        if new not in old_config:
            changes.append(f"NEW CONFIG: {new}\n")

    for old in old_config:  # checks for lines in the old config that don't exist in the new config
        if old not in new_config:
            changes.append(f"OLD CONFIG: {old}\n")

    return changes if changes else [f"No changes detected for {router_name}.\n"]

def main():
    results = {}

    for router, creds in ROUTER_CREDENTIALS.items():
        new_config = get_router_config(router, creds["hostname"], creds["username"], creds["password"])
        if new_config:
            results[router] = compare_configs(router, new_config)
        else:
            results[router] = [f"Failed to fetch config for {router}"]

    return results

