#!/usr/bin/env python3
# Quick Live Host Scanner - Command Line Version

import subprocess
import socket
import sys
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def ping_host(ip):
    """Check if host is alive"""
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                              capture_output=True, timeout=2)
        return result.returncode == 0
    except:
        return False

def scan_ports(ip):
    """Scan common ports on a host"""
    common_ports = [21, 22, 23, 25, 53, 80, 443, 3306, 3389, 8080]
    open_ports = []
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        if sock.connect_ex((ip, port)) == 0:
            open_ports.append(port)
        sock.close()
    
    return open_ports

def scan_network(network):
    """Scan a network range"""
    print(f"\n📡 Scanning network: {network}")
    print("="*50)
    
    try:
        net = ipaddress.ip_network(network, strict=False)
        hosts = list(net.hosts())
        
        if len(hosts) > 256:
            print(f"⚠️ Large network ({len(hosts)} IPs), scanning first 256")
            hosts = hosts[:256]
            
        live_hosts = []
        
        print(f"🔍 Scanning {len(hosts)} hosts...")
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_ip = {executor.submit(ping_host, str(ip)): str(ip) for ip in hosts}
            for future in future_to_ip:
                ip = future_to_ip[future]
                if future.result():
                    live_hosts.append(ip)
                    print(f"✅ {ip} - Alive")
                    
        print(f"\n📊 Found {len(live_hosts)} live hosts")
        
        # Port scan live hosts
        for ip in live_hosts:
            print(f"\n🔍 Scanning ports on {ip}:")
            ports = scan_ports(ip)
            if ports:
                print(f"   Open ports: {', '.join(str(p) for p in ports)}")
            else:
                print("   No common open ports found")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def scan_single(target):
    """Scan a single host"""
    print(f"\n🎯 Scanning: {target}")
    print("="*50)
    
    # Resolve domain if needed
    ip = target
    try:
        socket.inet_aton(target)
    except:
        try:
            ip = socket.gethostbyname(target)
            print(f"✅ Resolved to: {ip}")
        except:
            print("❌ Could not resolve domain")
            return
            
    # Check if alive
    if ping_host(ip):
        print(f"✅ {ip} is alive")
        
        # Scan ports
        print(f"\n🔍 Scanning ports...")
        ports = scan_ports(ip)
        if ports:
            print(f"Open ports: {', '.join(str(p) for p in ports)}")
        else:
            print("No common open ports found")
    else:
        print("❌ Host is not reachable")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 live_scanner.py <ip>")
        print("  python3 live_scanner.py <domain>")
        print("  python3 live_scanner.py <network> (e.g., 10.0.4.0/24)")
        sys.exit(1)
        
    target = sys.argv[1]
    
    if '/' in target:
        scan_network(target)
    else:
        scan_single(target)
