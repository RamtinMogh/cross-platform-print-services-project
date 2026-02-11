# Setup Guide - Cross-Platform Print Services

## Lab Environment
- Hypervisor: VMware Workstation
- VMs:
  - Windows 10 (Brasco - client)
  - Windows Server 2019 (BigGuy - print target + WSL host)
  - Debian 12 (ABC Server - native CUPS print server)
  - Linux Mint (ABC Client - client)
- All VMs on the same virtual network

## Step 1: Install CUPS and CUPS-PDF
On Debian 12 and Linux Mint:
sudo apt update
sudo apt install cups cups-pdf -y
sudo systemctl enable --now cups

## Step 2: Add CUPS-PDF Printer via Web Interface
Open http://localhost:631 (or server IP:631)
Administration → Add Printer → CUPS-PDF backend
Set name and location → Share printer

Names used:
- DebianPDF (on Debian ABC Server)
- WindowsServerPDF (in WSL on BigGuy Windows Server 2019)

## Step 3: Enable Remote Access (cupsd.conf)
Edit /etc/cups/cupsd.conf on both Debian and WSL:
Listen 0.0.0.0:631
Browsing On
WebInterface Yes
<Location />
  Order allow,deny
  Allow all
</Location>
<Location /admin>
  Order allow,deny
  Allow all
</Location>

Restart CUPS:
sudo systemctl restart cups

## Step 4: Install WSL + Ubuntu
On Windows Server 2019:
wsl --install -d Ubuntu

Launch Ubuntu in WSL and repeat Steps 1–3 (install CUPS, configure cupsd.conf, add CUPS-PDF printer).

## Step 5: Auto-Move Printed PDFs (Bash Script in WSL on Windows Server 2019)
Create the following script in WSL (Windows Server 2019):
```bash
#!/bin/bash
mv ~/PDF/* /mnt/c/Users/Public/Desktop/
```
Make executable:
chmod +x move_pdfs.sh
Add this line to /etc/cups/cups-pdf.conf (on both servers):
Out /mnt/c/Users/Public/Desktop/
Create the folder on Windows if it does not exist:
C:\Users\Public\Desktop\PrintedDocs
