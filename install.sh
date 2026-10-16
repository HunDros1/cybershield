#!/bin/bash
# Simple installation for CyberShield Lite

echo "🛡️ Installing CyberShield Lite..."
echo "================================"

# Install requirements
echo "📦 Installing packages..."
sudo apt update
sudo apt install -y python3 python3-pip python3-tk nmap
pip3 install python-nmap requests

# Make scripts executable
chmod +x cybershield_lite.py quick_scan.py

echo "✅ Installation complete!"
echo ""
echo "🚀 To start GUI: python3 cybershield_lite.py"
echo "🔍 Quick scan: python3 quick_scan.py example.com"
