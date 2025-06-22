import json
import subprocess
from scapy.all import sniff, IP, TCP, UDP
from logger import log_packet

# Load rules from JSON
with open("rules.json") as f:
    data = json.load(f)
FIREWALL_RULES = data.get("rules", [])


def matches_rule(packet):
    """
    Inspect packet against RULES. Return action ('block'/'allow') or None.
    """
    # Check IP rule
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        for rule in FIREWALL_RULES:
            if rule.get("ip") in (src, dst):
                return rule["action"]

    # Check TCP rule
    if TCP in packet:
        dport = packet[TCP].dport
        sport = packet[TCP].sport
        for rule in FIREWALL_RULES:
            if rule.get("protocol") == "tcp" and rule.get("port") in (dport, sport):
                return rule["action"]

    # Check UDP rule
    if UDP in packet:
        dport = packet[UDP].dport
        sport = packet[UDP].sport
        for rule in FIREWALL_RULES:
            if rule.get("protocol") == "udp" and rule.get("port") in (dport, sport):
                return rule["action"]

    return None


def apply_iptables(rule):
    """
    Apply system-level rule via iptables (requires sudo).
    """
    action = rule["action"]
    # Example: block IP
    if "ip" in rule:
        ip = rule["ip"]
        cmd = ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"] if action == "block" else ["iptables", "-A", "INPUT", "-s", ip, "-j", "ACCEPT"]
        subprocess.run(cmd)
    # Example: port rule
    if "port" in rule and "protocol" in rule:
        port = str(rule["port"])
        proto = rule["protocol"]
        target = "DROP" if action == "block" else "ACCEPT"
        cmd = ["iptables", "-A", "INPUT", "-p", proto, "--dport", port, "-j", target]
        subprocess.run(cmd)


def packet_callback(packet):
    """
    Callback for each sniffed packet: decide and log.
    """
    action = matches_rule(packet)
    summary = packet.summary()
    if action == "block":
        # Log and drop (stop processing)
        log_packet(summary, reason="Blocked by rule")
        return
    # If allowed or no matching rule
    print(f"[ALLOWED] {summary}")


def start_firewall(apply_system_rules: bool = False):
    """
    Begin sniffing and optionally apply iptables rules first.
    """
    print("[+] Starting Personal Firewall...")
    if apply_system_rules:
        for rule in FIREWALL_RULES:
            apply_iptables(rule)
    sniff(prn=packet_callback, store=False)
