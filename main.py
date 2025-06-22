from firewall import start_firewall
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Personal Firewall CLI")
    parser.add_argument("--iptables", action="store_true",
                        help="Apply rules via system iptables before sniffing")
    args = parser.parse_args()
    # Must run as sudo/root
    start_firewall(apply_system_rules=args.iptables)
