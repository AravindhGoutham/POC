#!/usr/bin/env python3

from netmiko import ConnectHandler
def configure_interface(mgmt_ip, password, interface_name=None, ipv4_address=None, ipv4_mask=None, ipv6_address=None, shutdown_action=None):
    try:
        device = {
            'device_type': 'cisco_ios',
            'ip': mgmt_ip,
            'username': 'admin',
            'password': password,
        }
        net_connect = ConnectHandler(**device)
        config_commands = []
        if interface_name:
            config_commands.append(f"interface {interface_name}")
            if ipv4_address and ipv4_mask:
                config_commands.append(f"ip address {ipv4_address} {ipv4_mask}")
            if ipv6_address:
                config_commands.append(f"ipv6 address {ipv6_address}")
            if shutdown_action:
                if shutdown_action.lower() == 'shutdown':
                    config_commands.append("shutdown")
                elif shutdown_action.lower() == 'no shutdown':
                    config_commands.append("no shutdown")
        if not config_commands:
            return False, "No interface configuration provided."
        output = net_connect.send_config_set(config_commands)
        net_connect.disconnect()
        return True, output
    except Exception as e:
        return False, str(e)

