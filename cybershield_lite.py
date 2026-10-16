#!/usr/bin/env python3
# CyberShield Lite - With SQL Injection Detection

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import socket
import requests
import threading
from datetime import datetime
import re
from urllib.parse import urlparse, urljoin

class CyberShieldLite:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ CyberShield Lite - SQLi Scanner")
        self.root.geometry("1100x750")
        self.root.configure(bg='#1a1a2e')
        
        self.target = tk.StringVar()
        self.scanning = False
        self.sqli_payloads = [
            "'",
            '"',
            "';--",
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--",
            "' AND SLEEP(5)--",
            "'; DROP TABLE users--",
            "' OR SLEEP(5)--",
            "1' AND '1'='1",
            "1' AND '1'='2",
        ]
        
        self.create_gui()
        self.log("🛡️ CyberShield Lite with SQLi Detection Ready!", "info")
        self.log("Enter domain (e.g., example.com) or IP address", "info")
        
    def create_gui(self):
        # Title
        title = tk.Label(self.root, text="🛡️ CYBERSHIELD LITE - SQLi SCANNER", 
                        font=('Arial', 18, 'bold'), fg='#00ff88', bg='#1a1a2e')
        title.pack(pady=10)
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg='#16213e', relief=tk.RIDGE, bd=2)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(input_frame, text="Target:", font=('Arial', 12), 
                fg='white', bg='#16213e').pack(side=tk.LEFT, padx=10)
        
        self.entry = tk.Entry(input_frame, textvariable=self.target, width=35,
                             font=('Arial', 12), bg='#0f3460', fg='white')
        self.entry.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(input_frame, text="(e.g., example.com)", font=('Arial', 10),
                fg='#88ccff', bg='#16213e').pack(side=tk.LEFT, padx=5)
        
        self.scan_btn = tk.Button(input_frame, text="🔍 SCAN", 
                                 command=self.start_scan, bg='#00ff88',
                                 fg='black', font=('Arial', 12, 'bold'),
                                 padx=20, cursor='hand2')
        self.scan_btn.pack(side=tk.LEFT, padx=10)
        
        self.clear_btn = tk.Button(input_frame, text="🗑️ CLEAR", 
                                  command=self.clear_all, bg='#ff6644',
                                  fg='white', font=('Arial', 12, 'bold'),
                                  padx=20, cursor='hand2')
        self.clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Main Content
        content = tk.Frame(self.root, bg='#1a1a2e')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left Panel - Results
        left_frame = tk.Frame(content, bg='#16213e', relief=tk.RIDGE, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Notebook for tabs
        notebook = ttk.Notebook(left_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1 - Main Results
        self.main_tab = tk.Frame(notebook, bg='#0f3460')
        notebook.add(self.main_tab, text="📊 Results")
        
        self.result_text = scrolledtext.ScrolledText(self.main_tab, height=20,
                                                    bg='#0f3460', fg='#00ff88',
                                                    font=('Courier', 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 2 - SQL Injection Detection
        self.sqli_tab = tk.Frame(notebook, bg='#0f3460')
        notebook.add(self.sqli_tab, text="💉 SQLi Detection")
        
        self.sqli_text = scrolledtext.ScrolledText(self.sqli_tab, height=20,
                                                  bg='#0f3460', fg='#ff8888',
                                                  font=('Courier', 10))
        self.sqli_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right Panel
        right_frame = tk.Frame(content, bg='#16213e', relief=tk.RIDGE, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10,0))
        
        # Status
        tk.Label(right_frame, text="📊 SCAN STATUS", font=('Arial', 12, 'bold'),
                fg='#88ccff', bg='#16213e').pack(pady=5)
        
        self.status_label = tk.Label(right_frame, text="Ready", font=('Arial', 14),
                                    fg='#00ff88', bg='#16213e')
        self.status_label.pack(pady=10)
        
        # Quick Info
        tk.Label(right_frame, text="ℹ️ QUICK INFO", font=('Arial', 12, 'bold'),
                fg='#88ccff', bg='#16213e').pack(pady=5)
        
        self.info_text = tk.Text(right_frame, height=12, width=30,
                                bg='#0f3460', fg='white', font=('Arial', 10))
        self.info_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Threat Level
        tk.Label(right_frame, text="⚠️ THREAT LEVEL", font=('Arial', 12, 'bold'),
                fg='#88ccff', bg='#16213e').pack(pady=5)
        
        self.threat_label = tk.Label(right_frame, text="🟢 LOW", 
                                    font=('Arial', 16, 'bold'),
                                    fg='#00ff88', bg='#16213e')
        self.threat_label.pack(pady=10)
        
        # SQLi Status
        tk.Label(right_frame, text="💉 SQLi VULNERABILITY", font=('Arial', 12, 'bold'),
                fg='#88ccff', bg='#16213e').pack(pady=5)
        
        self.sqli_label = tk.Label(right_frame, text="✅ NOT DETECTED", 
                                  font=('Arial', 14, 'bold'),
                                  fg='#00ff88', bg='#16213e')
        self.sqli_label.pack(pady=10)
        
        # Console
        console_frame = tk.Frame(self.root, bg='#0f3460', relief=tk.RIDGE, bd=2)
        console_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(console_frame, text="📝 Console", font=('Arial', 10, 'bold'),
                fg='white', bg='#0f3460').pack(anchor=tk.W, padx=10, pady=5)
        
        self.console = scrolledtext.ScrolledText(console_frame, height=5,
                                                 bg='black', fg='#00ff88',
                                                 font=('Courier', 9))
        self.console.pack(fill=tk.X, padx=5, pady=5)
        
    def extract_domain(self, target):
        """Extract domain from URL"""
        target = re.sub(r'^https?://', '', target)
        target = target.split('/')[0]
        target = target.split(':')[0]
        return target
        
    def log(self, message, level="info"):
        """Log to console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        emoji = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌", "sqli": "💉"}
        self.console.insert(tk.END, f"[{timestamp}] {emoji.get(level, '•')} {message}\n")
        self.console.see(tk.END)
        self.root.update()
        
    def update_status(self, text, color='#00ff88'):
        self.status_label.config(text=text, fg=color)
        self.root.update()
        
    def display_result(self, text, color='white'):
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.root.update()
        
    def display_sqli_result(self, text, color='#ff8888'):
        self.sqli_text.insert(tk.END, text + "\n")
        self.sqli_text.see(tk.END)
        self.root.update()
        
    def update_threat_level(self, level):
        colors = {
            "LOW": ("🟢 LOW", '#00ff88'),
            "MEDIUM": ("🟡 MEDIUM", '#ffcc00'),
            "HIGH": ("🟠 HIGH", '#ff8800'),
            "CRITICAL": ("🔴 CRITICAL", '#ff0000')
        }
        text, color = colors.get(level.upper(), ("🟢 LOW", '#00ff88'))
        self.threat_label.config(text=text, fg=color)
        
    def update_sqli_status(self, vulnerable, count=0):
        if vulnerable:
            self.sqli_label.config(text=f"⚠️ VULNERABLE ({count})", fg='#ff0000')
        else:
            self.sqli_label.config(text="✅ NOT DETECTED", fg='#00ff88')
            
    def start_scan(self):
        target = self.target.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a target!")
            return
            
        clean_target = self.extract_domain(target)
        if clean_target != target:
            self.log(f"Extracted domain: {clean_target}", "info")
            self.target.set(clean_target)
            target = clean_target
            
        if self.scanning:
            return
            
        self.scan_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)
        self.scanning = True
        
        self.result_text.delete(1.0, tk.END)
        self.sqli_text.delete(1.0, tk.END)
        self.info_text.delete(1.0, tk.END)
        self.update_status("Scanning...", '#ffcc00')
        
        thread = threading.Thread(target=self.perform_scan, args=(target,))
        thread.daemon = True
        thread.start()
        
    def perform_scan(self, target):
        try:
            self.log(f"Starting comprehensive scan on {target}", "info")
            self.display_result("="*60)
            self.display_result(f"🎯 SCANNING: {target}")
            self.display_result("="*60)
            
            # Domain resolution
            is_ip = self.is_ip(target)
            if not is_ip:
                self.log(f"Resolving domain {target}...", "info")
                ip = self.resolve_domain(target)
                if ip:
                    self.display_result(f"✅ IP Address: {ip}")
                    self.log(f"Resolved to {ip}", "success")
                else:
                    self.display_result("❌ Could not resolve domain")
                    self.log("Domain resolution failed", "error")
                    return
            else:
                ip = target
                self.display_result(f"✅ IP Address: {ip}")
            
            # Ping test
            self.display_result("\n📡 PING TEST:")
            ping = self.ping_host(ip)
            if ping:
                self.display_result(f"✅ Host is reachable ({ping}ms)")
            else:
                self.display_result("❌ Host is not reachable")
            
            # Port scan
            self.display_result("\n🔌 PORT SCAN:")
            self.update_status("Scanning ports...", '#ffcc00')
            open_ports = self.scan_ports(ip)
            
            if open_ports:
                self.display_result(f"✅ Found {len(open_ports)} open ports:")
                for port in open_ports:
                    self.display_result(f"   • Port {port}")
            else:
                self.display_result("✅ No common open ports found")
            
            # Web server check
            if not is_ip:
                self.display_result("\n🌐 WEB SERVER:")
                self.check_web_server(target)
            
            # SQL Injection Detection - NEW
            self.display_result("\n💉 SQL INJECTION DETECTION:")
            self.display_sqli_result("="*60)
            self.display_sqli_result("💉 SQL INJECTION SCAN RESULTS")
            self.display_sqli_result("="*60)
            
            sqli_results = self.detect_sql_injection(target)
            
            if sqli_results['vulnerable']:
                self.display_result(f"⚠️ SQL INJECTION VULNERABILITY DETECTED!")
                self.display_result(f"   Found {len(sqli_results['vulnerable_params'])} vulnerable parameter(s)")
                self.log(f"SQL Injection detected! {len(sqli_results['vulnerable_params'])} params vulnerable", "sqli")
                
                self.display_sqli_result("⚠️ VULNERABLE PARAMETERS FOUND:")
                for param, payloads in sqli_results['vulnerable_params'].items():
                    self.display_sqli_result(f"\n📌 Parameter: {param}")
                    self.display_sqli_result(f"   Vulnerable to: {', '.join(payloads)}")
                    self.display_sqli_result(f"   Risk: HIGH")
                
                self.update_sqli_status(True, len(sqli_results['vulnerable_params']))
            else:
                self.display_result("✅ No SQL injection vulnerabilities detected")
                self.log("No SQL injection vulnerabilities found", "success")
                self.display_sqli_result("✅ No SQL injection vulnerabilities detected")
                self.update_sqli_status(False)
            
            # Vulnerability check
            self.display_result("\n⚠️ VULNERABILITY CHECK:")
            vulns = self.check_vulnerabilities(ip, open_ports)
            
            # Add SQLi to vulnerabilities if found
            if sqli_results['vulnerable']:
                vulns.append(f"SQL Injection vulnerability in {len(sqli_results['vulnerable_params'])} parameter(s)")
            
            if vulns:
                self.display_result(f"⚠️ Found {len(vulns)} potential issues:")
                for vuln in vulns:
                    self.display_result(f"   • {vuln}")
            else:
                self.display_result("✅ No obvious vulnerabilities found")
            
            # Calculate threat level
            threat_level = self.calculate_threat_level(open_ports, vulns, sqli_results)
            self.display_result(f"\n📊 THREAT LEVEL: {threat_level.upper()}")
            self.update_threat_level(threat_level)
            
            # Update quick info
            self.update_info(target, ip, open_ports, vulns, threat_level, sqli_results)
            
            self.display_result("\n" + "="*60)
            self.display_result("✅ SCAN COMPLETE!")
            self.display_result("="*60)
            
            self.update_status("Scan Complete", '#00ff88')
            self.log("Scan completed successfully!", "success")
            
        except Exception as e:
            self.display_result(f"\n❌ ERROR: {str(e)}")
            self.log(f"Error: {str(e)}", "error")
        finally:
            self.scanning = False
            self.scan_btn.config(state=tk.NORMAL)
            self.clear_btn.config(state=tk.NORMAL)
            
    def detect_sql_injection(self, domain):
        """Detect SQL injection vulnerabilities"""
        results = {
            'vulnerable': False,
            'vulnerable_params': {},
            'tests_performed': 0
        }
        
        # Try to find forms and parameters on the site
        try:
            # First, check if there are any forms or parameters
            self.display_sqli_result("🔍 Searching for input parameters...")
            
            # Common parameters to test
            test_params = ['id', 'page', 'cat', 'product', 'user', 'q', 'query', 'search']
            
            # Check for common pages with parameters
            test_urls = [
                f"http://{domain}",
                f"https://{domain}",
                f"http://{domain}/index.php",
                f"http://{domain}/page.php",
                f"http://{domain}/product.php",
                f"http://{domain}/details.php"
            ]
            
            found_parameters = []
            
            # Try to find parameters by checking common URLs
            for url in test_urls:
                try:
                    response = requests.get(url, timeout=5, verify=False)
                    # Look for links with parameters
                    links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
                    for link in links:
                        if '?' in link:
                            params = link.split('?')[1].split('&')
                            for param in params:
                                if '=' in param:
                                    param_name = param.split('=')[0]
                                    if param_name not in found_parameters:
                                        found_parameters.append(param_name)
                except:
                    pass
                    
            # If no parameters found, use common ones
            if not found_parameters:
                found_parameters = test_params
                
            self.display_sqli_result(f"📋 Testing {len(found_parameters)} parameter(s): {', '.join(found_parameters[:5])}...")
            
            # Test each parameter with SQL injection payloads
            for param in found_parameters[:5]:  # Limit to 5 parameters to avoid too many requests
                self.display_sqli_result(f"\n🧪 Testing parameter: {param}")
                
                for payload in self.sqli_payloads[:8]:  # Test top payloads
                    try:
                        test_url = f"http://{domain}/?{param}={payload}"
                        response = requests.get(test_url, timeout=5, verify=False)
                        
                        # Check for SQL injection indicators
                        error_patterns = [
                            r'SQL syntax',
                            r'MySQL',
                            r'ORA-',
                            r'PostgreSQL',
                            r'SQLite',
                            r'Microsoft OLE DB',
                            r'Unclosed quotation mark',
                            r'You have an error in your SQL syntax',
                            r'Warning: mysql_',
                            r'Warning: mysqli_',
                            r'Database error',
                            r'Invalid query',
                            r'SQLSTATE'
                        ]
                        
                        # Check for time-based indicators
                        if 'SLEEP' in payload and response.elapsed.total_seconds() > 4:
                            results['vulnerable'] = True
                            if param not in results['vulnerable_params']:
                                results['vulnerable_params'][param] = []
                            results['vulnerable_params'][param].append('Time-based SQLi')
                            self.display_sqli_result(f"   ⚠️ Time-based SQLi with: {payload}")
                            break
                            
                        # Check for error-based indicators
                        for pattern in error_patterns:
                            if re.search(pattern, response.text, re.IGNORECASE):
                                results['vulnerable'] = True
                                if param not in results['vulnerable_params']:
                                    results['vulnerable_params'][param] = []
                                results['vulnerable_params'][param].append('Error-based SQLi')
                                self.display_sqli_result(f"   ⚠️ Error-based SQLi with: {payload}")
                                self.display_sqli_result(f"   Pattern detected: {pattern}")
                                break
                                
                        # Check for boolean-based indicators
                        if "' AND '1'='1" in payload or "' AND '1'='2" in payload:
                            # Test two different boolean conditions
                            url_true = f"http://{domain}/?{param}=1' AND '1'='1"
                            url_false = f"http://{domain}/?{param}=1' AND '1'='2"
                            try:
                                resp_true = requests.get(url_true, timeout=5, verify=False)
                                resp_false = requests.get(url_false, timeout=5, verify=False)
                                if resp_true.text != resp_false.text:
                                    results['vulnerable'] = True
                                    if param not in results['vulnerable_params']:
                                        results['vulnerable_params'][param] = []
                                    results['vulnerable_params'][param].append('Boolean-based SQLi')
                                    self.display_sqli_result(f"   ⚠️ Boolean-based SQLi detected")
                                    break
                            except:
                                pass
                                
                        results['tests_performed'] += 1
                        
                    except:
                        pass
                        
            # Summary
            self.display_sqli_result("\n" + "="*60)
            if results['vulnerable']:
                self.display_sqli_result(f"⚠️ SQL INJECTION VULNERABLE: {len(results['vulnerable_params'])} parameter(s) affected")
                for param in results['vulnerable_params']:
                    self.display_sqli_result(f"   - {param}: {', '.join(results['vulnerable_params'][param])}")
            else:
                self.display_sqli_result("✅ No SQL injection vulnerabilities detected")
            self.display_sqli_result(f"📊 Tests performed: {results['tests_performed']}")
            self.display_sqli_result("="*60)
            
        except Exception as e:
            self.display_sqli_result(f"❌ SQLi scan error: {str(e)}")
            self.log(f"SQLi scan error: {str(e)}", "error")
            
        return results
        
    def is_ip(self, target):
        try:
            socket.inet_aton(target)
            return True
        except:
            return False
            
    def resolve_domain(self, domain):
        try:
            return socket.gethostbyname(domain)
        except:
            return None
            
    def ping_host(self, ip):
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                                  capture_output=True, timeout=3)
            if result.returncode == 0:
                output = result.stdout.decode()
                if 'time=' in output:
                    return output.split('time=')[1].split(' ')[0]
                return "0"
            return None
        except:
            return None
            
    def scan_ports(self, ip):
        common_ports = [21, 22, 23, 25, 53, 80, 443, 3306, 3389, 5432, 6379, 8080, 8443]
        open_ports = []
        
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            sock.close()
            
        return open_ports
        
    def check_web_server(self, domain):
        try:
            response = requests.get(f"http://{domain}", timeout=3)
            self.display_result(f"✅ HTTP Server running (Status: {response.status_code})")
            self.log(f"Web server detected: HTTP {response.status_code}", "info")
            
            try:
                response = requests.get(f"https://{domain}", timeout=3, verify=False)
                self.display_result(f"✅ HTTPS Server running (Status: {response.status_code})")
                self.log(f"HTTPS server detected", "info")
            except:
                self.display_result("⚠️ HTTPS not available")
                
        except:
            self.display_result("❌ No web server detected")
            
    def check_vulnerabilities(self, ip, open_ports):
        vulns = []
        
        dangerous_ports = {
            21: "FTP - Unencrypted file transfer",
            23: "Telnet - Unencrypted remote access",
            25: "SMTP - Email server exposed",
            3306: "MySQL - Database exposed",
            3389: "RDP - Remote desktop exposed",
            5432: "PostgreSQL - Database exposed",
            6379: "Redis - In-memory database exposed"
        }
        
        for port in open_ports:
            if port in dangerous_ports:
                vulns.append(dangerous_ports[port])
                
        if 80 in open_ports and 443 not in open_ports:
            vulns.append("HTTP without HTTPS - Data not encrypted")
            
        return vulns
        
    def calculate_threat_level(self, open_ports, vulns, sqli_results):
        score = 0
        
        if open_ports:
            score += len(open_ports) * 2
            
        if vulns:
            score += len(vulns) * 3
            
        # Add extra weight for SQL injection
        if sqli_results.get('vulnerable', False):
            score += 10
            
        if score == 0:
            return "LOW"
        elif score <= 5:
            return "LOW"
        elif score <= 10:
            return "MEDIUM"
        elif score <= 15:
            return "HIGH"
        else:
            return "CRITICAL"
            
    def update_info(self, target, ip, open_ports, vulns, threat_level, sqli_results):
        info = f"Target: {target}\n"
        info += f"IP: {ip}\n"
        info += f"Open Ports: {len(open_ports)}\n"
        info += f"Vulnerabilities: {len(vulns)}\n"
        info += f"SQL Injection: {'⚠️ YES' if sqli_results.get('vulnerable', False) else '✅ NO'}\n"
        info += f"Threat Level: {threat_level}\n"
        info += f"Scan Time: {datetime.now().strftime('%H:%M:%S')}"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
        
    def clear_all(self):
        self.result_text.delete(1.0, tk.END)
        self.sqli_text.delete(1.0, tk.END)
        self.info_text.delete(1.0, tk.END)
        self.console.delete(1.0, tk.END)
        self.target.set('')
        self.update_status("Ready", '#00ff88')
        self.update_threat_level("LOW")
        self.update_sqli_status(False)
        self.log("Cleared all data", "info")
        
def main():
    root = tk.Tk()
    app = CyberShieldLite(root)
    root.mainloop()

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════╗
    ║  🛡️  CYBERSHIELD LITE - SQLi Scanner      ║
    ║  Advanced SQL Injection Detection Tool      ║
    ║  For Educational Use Only                  ║
    ╚══════════════════════════════════════════════╝
    """)
    main()
