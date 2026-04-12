# CodeAlpha_IDS_Project
Goal: Detect unauthorized network activity and automatically block the attacker.

1. The Setup
Attacker: Kali Linux (192.168.1.5)

IDS/Victim: Ubuntu (192.168.1.6) running Suricata.

Networking: Bridged mode with NIC offloading disabled for better packet capture.

2. Detection (IDS)
I configured a custom rules in local.rules to flag ICMP traffic (pings) and Nmap from the attacker.

Rules: alert icmp any any -> any any (msg:"ICMP Ping Detected"; sid:1000001; rev:1;)
     : alert tcp any any -> any any (flags:S; msg:"Possible Nmap SYN Scan"; sid:1000002; rev:1;)
     : alert tcp any any -> any any (msg:"Port Scan Detected"; flow:stateless; threshold:type both, track by_src, count 10, seconds 5; sid:1000003; rev:1;)
     
Result: Suricata successfully logged every attack in fast.log

3. Response (IPS)
I developed a Python script (ips.py) that acts as an Active Response mechanism.

How it works: The script monitors the Suricata log. When it sees an alert, it extracts the attacker’s IP and adds it to the Linux iptables firewall.

Key Feature: The script cleans the IP data (removing port numbers) and uses the -I command to ensure the block is the #1 priority in the firewall.

4. Conclusion
This project's main objective was to create and implement a working Network Security Monitoring environment with automatic mitigation and real-time threat detection. I was able to construct a visibility layer over network traffic and enable deep packet inspection of incoming requests by integrating Suricata as the primary detection engine within a virtualised Linux system.

The project transformed into a dynamic security automation pipeline during deployment from a simple signature-based detection system. The Response phase received a lot of attention, and I created a unique Python-based middleware to connect system-level firewall orchestration with raw security logs.
