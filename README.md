# Grim Reaper

> [!IMPORTANT]
> **REQUIRES ROOT PRIVILEGES**
> Using `scapy` for ARP packet injection doesn't work without privileges.

I created this script because I was bored in my psychology class.

Basically, I wanted something that looked good on the terminal while I was wasting time in class. It's a tool for spying on the network and finding out who's connected, similar to [arp-scan](https://github.com/royhills/arp-scan) or [netdiscover](https://github.com/netdiscover-scanner/netdiscover), with the difference that with this one you can save the results in a `.txt` file and also search for MAC addresses in [MacVendors](https://macvendors.com/).

## Features

- **ARP scanning** — discover devices on your network
- **MAC vendor lookup** — identify device manufacturers
- **Save results** — export scans to `.txt` files
- **Colorful terminal output** — powered by `rich` and `termcolor`

## Installation

```bash
git clone https://github.com/Sn0wBaall/Grim-Reaper.git
cd Grim-Reaper
pip install -r requirements.txt
```

## Usage

```
MAC Checker:
	-m              Uniq MAC
	-M              MAC file
	-t, --threads   Threads number

ARP scanner (EXECUTE IT AS ROOT):
	-r, --range     IP range
	-i, --interface Network interface
	-c, --complete  ARP scan and check MAC's

General:
	-h, --help      Show this help panel
```

### ARP scan

```bash
sudo python3 Grim_Reaper.py -r 192.168.1.0/24 -i eth0
```

### Complete scan (ARP + MAC lookup)

```bash
sudo python3 Grim_Reaper.py -c -r 192.168.1.0/24 -i eth0
```

### MAC vendor lookup

```bash
python3 Grim_Reaper.py -m 00:11:22:33:44:55
python3 Grim_Reaper.py -M macs.txt -t 10
```

## Screenshots

![Image](Images/Image1.png)

### ARP scan

![Image](Images/Image2.png)

### Complete scan

![Image](Images/Image3.png)

## Disclaimer

This tool is intended for educational purposes and network troubleshooting on networks you own or have permission to scan.
