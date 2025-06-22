from datetime import datetime

def log_packet(packet_summary: str, reason: str = ""):
    """
    Append a timestamped log entry with packet summary and reason to firewall.og_txt.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("firewall.log_txt", "a") as f:
        f.write(f"{timestamp} - {reason} - {packet_summary}\n")
