#!/usr/bin/env python3

from netmiko import ConnectHandler

def configure_dhcpv6(mgmt_ip, password, pool_name, ipv6_prefix, prefix_length, dns_server, domain_name, interface_name):
    try:
        device = {
            'device_type': 'cisco_ios',
            'ip': mgmt_ip,
            'username': 'admin',
            'password': password,
        }
        net_connect = ConnectHandler(**device)

        config_commands = [
            f"ipv6 dhcp pool {pool_name}",
            f"address prefix {ipv6_prefix}/{prefix_length}",
            f"dns-server {dns_server}",
            f"domain-name {domain_name}",
        ]
        output_pool = net_connect.send_config_set(config_commands)

        interface_commands = [
            f"interface {interface_name}",
            "ipv6 enable",
            f"ipv6 dhcp server {pool_name}"
        ]
        output_interface = net_connect.send_config_set(interface_commands)

        net_connect.disconnect()

        return True, output_pool + "\n" + output_interface

    except Exception as e:
        return False, str(e)
