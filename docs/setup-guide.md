# Setup Guide - Cross-Platform Print Services

This guide documents the exact steps I followed to build and verify the solution in a VMware lab environment. All commands assume root/sudo access where needed.

## Lab Environment Overview
- Hypervisor: VMware Workstation
- VMs & roles:
  - Windows 10 → Client (Brasco)
  - Windows Server 2019 → Print target + WSL host (BigGuy)
  - Debian 12 → CUPS print server (ABC Server)
  - Linux Mint → Client (ABC Client)
- Networking: All VMs on the same virtual network (e.g., NAT or VMnet)

## Step 1: Prepare CUPS on Debian 12 (ABC Server - native Linux CUPS)
```bash
sudo apt update
sudo apt install cups cups-pdf -y
sudo systemctl enable --now cups
Edit /etc/cups/cupsd.conf to allow remote access:

Replace Listen localhost:631 with Listen 0.0.0.0:631
Under <Location /> and <Location /admin> add:textOrder allow,deny
Allow all
Enable web interface: WebInterface Yes
Enable browsing: Browsing On

Restart CUPS:
Bashsudo systemctl restart cups
Add the virtual PDF printer:

Open browser → http://<debian-ip>:631
Administration → Add Printer → Local Printers → CUPS-PDF (or "Generic CUPS-PDF Printer")

Name it e.g. DebianPDF
Step 2: CUPS inside WSL on Windows Server 2019 (BigGuy)
On Windows Server 2019:

Enable WSL → Install Ubuntu from Microsoft Store or wsl --install -d Ubuntu
Launch Ubuntu in WSL

Inside WSL terminal:
Bashsudo apt update && sudo apt install cups cups-pdf -y
sudo systemctl enable --now cups
Apply same cupsd.conf changes as above (use sudo nano /etc/cups/cupsd.conf).
Add CUPS-PDF printer via web interface (http://localhost:631 from WSL, or network IP from host).
Name it e.g. WindowsServerPDF
Step 3: Configure Post-Print PDF Relocation
Edit /etc/cups/cups-pdf.conf (in both CUPS instances):

Set output directory to Windows-accessible path:textOut /mnt/c/Users/Public/Desktop/PrintedDocs/

Create the target folder on Windows:

C:\Users\Public\Desktop\PrintedDocs (create if missing)

Step 4: Deploy Flask PDF Upload Portal (in WSL on Windows Server)
In WSL:
Bashsudo apt install python3-pip -y
pip install flask
mkdir flask-app && cd flask-app
Create app.py (see flask-app/app.py in repo for full code).
Run the app:
Bashpython3 app.py
The portal will be available at http://<wsl-ip>:5000 (find WSL IP with ip addr show eth0 or hostname -I).
From Windows 10 client:

Open browser → http://<wsl-ip>:5000
Upload PDF → Select printer (DebianPDF or WindowsServerPDF) → Submit

Step 5: Client-Side Printing (Linux Mint → CUPS printers)
On Linux Mint:

Settings → Printers → Add Printer
Network Printer → Internet Printing Protocol (ipp://<server-ip>:631/printers/DebianPDF)
Or discover via Bonjour/mDNS if Browsing is enabled

Verification Checklist

Upload PDF via Flask from Windows 10 → appears in CUPS queue → PDF lands in C:\Users\Public\Desktop\PrintedDocs
Print test page from Linux Mint to both CUPS queues → confirm output
Check CUPS web UI for job history and status

Notes: Firewall rules may need ufw allow 631 on Debian/WSL hosts. WSL networking requires Windows host firewall to allow inbound 5000/631 if testing externally.
