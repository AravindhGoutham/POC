#!/usr/bin/env python3

from flask import Flask, render_template, request, send_from_directory
import getconfig
import diffconfig
import dhcpv4config
import interfaceconfig

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/getconfig')
def getconfig_page():
    files = getconfig.configurations()
    return render_template("getconfig.html", files=files)

@app.route('/diffconfig')
def diff_config_page():
    results = diffconfig.main()
    return render_template("diffconfig.html", results=results)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(os.getcwd(), filename, as_attachment=True)

@app.route('/dhcpv4')
def dhcpv4_page():
    return render_template('dhcpv4config.html')

@app.route('/dhcpv4submit', methods=['POST'])
def dhcpv4_submit():
    if request.method == 'POST':
        mgmt_ip = request.form.get('mgmt_ip')
        password = request.form.get('password')
        pool_name = request.form.get('pool_name')
        network_address = request.form.get('network_address')
        subnet_mask = request.form.get('subnet_mask')
        default_gateway = request.form.get('default_gateway')
        dns_server = request.form.get('dns_server')

        success, message = dhcpv4config.configure_dhcpv4(
            mgmt_ip, password, pool_name, network_address, subnet_mask, default_gateway, dns_server
        )

        if success:
            return f"DHCPv4 Configuration Successful on {mgmt_ip}!"
        else:
            return f"Error: {message}", 500

@app.route('/interfaceconfig')
def interface_config_page():
    return render_template('interfaceconfig.html')

@app.route('/interfaceconfigsubmit', methods=['POST'])
def interface_config_submit():
    if request.method == 'POST':
        mgmt_ip = request.form.get('mgmt_ip')
        password = request.form.get('password')
        interface_name = request.form.get('interface_name')
        ipv4_address = request.form.get('ipv4_address')
        ipv4_mask = request.form.get('ipv4_mask')
        ipv6_address = request.form.get('ipv6_address')
        shutdown_action = request.form.get('shutdown_action')
        success, message = interfaceconfig.configure_interface(
            mgmt_ip, password, interface_name, ipv4_address, ipv4_mask, ipv6_address, shutdown_action
        )
        if success:
            return f"Interface Configuration Successful on {mgmt_ip}!"
        else:
            return f"Error: {message}", 500
if __name__ == '__main__':
    app.run(debug=True, port=80)

