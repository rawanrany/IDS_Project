import subprocess
import time
import os

LOG_FILE = "/var/log/suricata/fast.log"

def block_ip(ip):
    # This function now uses -I and 1 to ensure the rule is at the top
    print(f"[!] ACTION: Executing firewall block on {ip}...")
    subprocess.run(["sudo", "iptables", "-I", "INPUT", "1", "-s", ip, "-j", "DROP"])
    print(f"[SUCCESS] {ip} is now blocked at the top of the firewall.")

with open(LOG_FILE, "r") as f:
    f.seek(0, os.SEEK_END)
    print("IDS Response System is running... waiting for attacks.")

    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        
        # Check for your ICMP alert
        if "ICMP" in line.upper():
            parts = line.split()
            try:
                idx = parts.index("->")
                raw_ip = parts[idx - 1] # This might be '192.168.1.5:8'
                
                # --- THIS IS THE NEW PART ---
                # Split by ':' and take the first part to get just the IP
                attacker_ip = raw_ip.split(':')[0] 
                # ----------------------------

                block_ip(attacker_ip)
            except Exception as e:
                print(f"Parsing error: {e}")
