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

```bash
sudo apt update
sudo apt install cups cups-pdf -y
sudo systemctl enable --now cups
```

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
wsl --install -d Ubuntu-20.04

Launch Ubuntu in WSL and repeat Steps 1–3 (install CUPS, configure cupsd.conf, add CUPS-PDF printer).

## Step 5: Auto-Move Printed PDFs (Bash Script in WSL on Windows Server 2019)
Create the following script in WSL (Windows Server 2019):
```bash
#!/bin/bash
mv ~/PDF/* /mnt/c/Users/Public/Desktop/
```
- Make executable: chmod +x move_pdfs.sh
- Add this line to /etc/cups/cups-pdf.conf (on both servers):
  - Out /mnt/c/Users/Public/Desktop/

See the full script file: [move_pdfs.sh](../scripts/move_pdfs.sh)

## Step 6: Flask PDF Upload Portal (in WSL on Windows 10)
In WSL:
sudo apt install python3-pip -y
pip install flask
mkdir flask-app && cd flask-app

Create app.py — full source code: [flask-app/app.py](../flask-app/app.py)

Run:
python3 app.py

Access from Windows 10 browser: http://<wsl-ip>:5000
(Find WSL IP: ip addr show eth0 or hostname -I)

## Step 7: Add Shared CUPS Printers on Clients
On Linux Mint (ABC Client):
Settings → Printers → Add Printer
Network Printer → Internet Printing Protocol (IPP)
URL example: ipp://<debian-ip>:631/printers/DebianPDF
or ipp://<wsl-ip>:631/printers/WindowsServerPDF

On Windows 10 (Brasco):
Use browser to http://<wsl-ip>:5000
Upload PDF → Select printer → Submit (Flask handles submission to CUPS)

## Verification Steps
- Upload PDF from Windows 10 via Flask portal → check CUPS job queue[](http://<server-ip>:631) 
- Print test page from Linux Mint to both printers → confirm PDF appears
- View all jobs and status at http://<server-ip>:631

## Additional Notes
- Firewall: Allow port 631 (CUPS) and 5000 (Flask)
  Debian/WSL: sudo ufw allow 631
  Windows firewall: allow inbound 631 and 5000
- Troubleshooting: Check CUPS error log (/var/log/cups/error_log) if jobs fail
- No Samba used — all sharing via HTTP/IPP

See full original proposal: [BigGuy Corp Multi-access Print Services Proposal](../docs/BigGuy-Corp-Print-Services-Proposal.pdf)
