# 🕷️ ARP Poisoning Script (Python)

This Python script allows you to perform **ARP Poisoning** (also known as ARP Spoofing) on a local network. It tricks both the target machine and the router into routing their traffic through your device, enabling a basic **Man-in-the-Middle** (MITM) setup.

---

## 📌 Features

- Crafting and sending raw packets using Scapy
- Bidirectional ARP poisoning between target and router
- Automatically resets ARP tables when stopped (Ctrl+C)
- Modern `argparse` support for command-line arguments

---

## 🧪 Requirements

- Python 3
- [Scapy](https://scapy.readthedocs.io/en/latest/)

To install Scapy:

```bash
sudo pip install scapy
```

> If you're using Kali Linux and `pip` doesn't work:
> ```bash
> sudo apt install python3-scapy
> ```

---

## 🚀 Usage

### Run the script:

```bash
sudo python3 arpPoison.py -t <TARGET_IP> -g <GATEWAY_IP>
```

### Example:

```bash
sudo python3 arpPoison.py -t 192.168.1.10 -g 192.168.1.1
```

> ❗ **sudo** is required since the script sends low-level network packets.

---

## 📂 Code Explanation

### 🔍 `get_mac_address(ip)`
Sends an ARP request to the given IP and returns the MAC address of the first device that responds.

### ⚔️ `arp_poisoning(target_ip, poisoned_ip)`
Sends a fake ARP response to the target, telling it that the poisoned IP is at the attacker's MAC address.

### ♻️ `reset_operation(fooled_ip, gateway_ip)`
Restores the ARP table by sending the correct MAC address for the gateway or the target. Automatically called on script exit (Ctrl+C).

### ⚙️ `argparse`
Handles input parameters from the command line:
- `-t` / `--target`: IP address of the target device
- `-m` / `--modem`: IP address of the gateway/router

---

## 🧠 What is ARP Poisoning?

**ARP Poisoning** is a network attack technique that sends spoofed ARP messages to a LAN. It associates the attacker's MAC address with the IP address of another device (usually the gateway), redirecting traffic through the attacker. This forms the basis of **Man-in-the-Middle** attacks.

---

## 🛑 Exit and Cleanup

When you press **Ctrl+C**:
- The script sends correct ARP responses to fix the ARP tables.
- Network communication should return to normal.

---

