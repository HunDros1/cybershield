#!/usr/bin/env python3
# Quick command-line scanner

import socket
import subprocess
import sys

def quick_scan(target):
    print("🛡️ CyberShield Lite - Quick Scan")
    print("="*40)
    
    # Ping
    print("📡 Checking host...")
    try:
        subprocess.run(['ping', '-c', '1', target], check=True, timeout=3)
        print("✅ Host is reachable")
    except:
        print("❌ Host not reachable")
        return
        
    # Port scan
    print("\n🔍 Scanning common ports...")
    ports = [21, 22, 23, 25, 80, 443, 3306, 3389]
    open_ports = []
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((target, port)) == 0:
            open_ports.append(port)
        sock.close()
        
    if open_ports:
        print(f"⚠️ Open ports: {', '.join(str(p) for p in open_ports)}")
    else:
        print("✅ No common open ports found")
        
    # Quick vulnerability check
    print("\n⚠️ Quick check:")
    if 80 in open_ports and 443 not in open_ports:
        print("   • HTTP without HTTPS")
    if 21 in open_ports:
        print("   • FTP service exposed")
    if 23 in open_ports:
        print("   • Telnet service exposed")
    if 3306 in open_ports:
        print("   • MySQL database exposed")
        
    print("\n✅ Scan complete!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 quick_scan.py <target>")
        sys.exit(1)
    quick_scan(sys.argv[1])
