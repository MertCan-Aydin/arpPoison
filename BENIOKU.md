# 🕷️ ARP Poisoning Script (Python)

Bu Python scripti, bir yerel ağda **ARP Poisoning (ARP Zehirleme)** saldırısı gerçekleştirmenizi sağlar. Hedef makineyi ve yönlendiriciyi kandırarak, aradaki trafiği kendi cihazınız üzerinden geçirmenize olanak tanır (**Man-in-the-Middle** saldırısı için temel bir yapı).

---

## 📌 Özellikler

- Scapy ile ham paket oluşturma ve gönderme
- Hedef ve modem IP’leri üzerinden çift taraflı ARP zehirleme
- ARP tablolarını eski haline döndürme (Ctrl+C ile çıkınca)
- Modern `argparse` ile komut satırı parametreleri desteği

---

## 🧪 Gereksinimler

- Python 3
- [Scapy](https://scapy.readthedocs.io/en/latest/)

Scapy'yi yüklemek için:

```bash
sudo pip install scapy
```

> Kali Linux kullanıyorsanız ve pip kullanılamıyorsa:
> ```bash
> sudo apt install python3-scapy
> ```

---

## 🚀 Kullanım

### Script’i çalıştırmak için:

```bash
sudo python3 arpPoison.py -t <HEDEF_IP> -g <GATEWAY_IP>
```

### Örnek:

```bash
sudo python3 arpPoison.py -t 192.168.1.10 -g 192.168.1.1
```

> ❗ **sudo** kullanmanız gereklidir çünkü ağ paketleri gönderiyorsunuz.

---

## 📂 Kodun Açıklaması

### 🔍 `get_mac_address(ip)`
Verilen IP adresine ait MAC adresini döndürür. Yayın adresine ARP isteği gönderip, ilk cevap verenin MAC adresini alır.

### ⚔️ `arp_poisoning(target_ip, poisoned_ip)`
Hedef cihazı kandırmak için sahte bir ARP yanıtı gönderir. Böylece hedef, `poisoned_ip`’nin MAC adresi olarak saldırganı kaydeder.

### ♻️ `reset_operation(fooled_ip, gateway_ip)`
Saldırı sonrası cihazlara doğru ARP bilgisi göndererek ağ tablosunu düzeltir. (Ctrl+C ile çıkıldığında otomatik çalışır.)

### ⚙️ `argparse`
Kullanıcıdan komut satırı üzerinden hedef ve gateway IP’leri alınır:
- `-t` / `--target`: Hedef cihazın IP adresi
- `-m` / `--modem`: Modem / yönlendiricinin IP adresi

---

## 🧠 ARP Zehirleme Nedir?

**ARP Poisoning**, ağdaki cihazlara sahte ARP yanıtları göndererek IP adreslerini yanlış MAC adresleriyle eşleştirmesini sağlamak için kullanılan bir saldırı türüdür. Saldırgan, iki cihaz (örneğin hedef ve gateway) arasında kendisini konumlandırarak tüm trafiği gözetleyebilir ya da değiştirebilir.

---

## 🛑 Çıkış ve Temizlik

Script çalışırken **Ctrl+C** tuşlarına basarsanız:
- ARP tabloları eski haline döner
- Ağda iletişim normale döner

---
