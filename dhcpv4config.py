#!/usr/bin/env python3

from netmiko import ConnectHandler
def configure_dhcpv4(mgmt_ip, password, pool_name, network_address, subnet_mask, default_gateway, dns_server):
    try:
        device = {
            'device_type': 'cisco_ios',
            'ip': mgmt_ip,
            'username': 'admin',
            'password': password,
        }
        net_connect = ConnectHandler(**device)
        config_commands = [
            f"ip dhcp excluded-address {default_gateway} {default_gateway}",
            f"ip dhcp pool {pool_name}",
            f"network {network_address} {subnet_mask}",
            f"default-router {default_gateway}",
            f"dns-server {dns_server}",
        ]
        output = net_connect.send_config_set(config_commands)
        net_connect.disconnect()
        return True, output
    except Exception as e:
        return False, str(e)
