# Setup Guide - Cross-Platform Print Services

This guide follows the exact implementation steps from the original BigGuy Corp proposal (pages 7–10).

## Lab Environment
- Hypervisor: VMware Workstation
- VMs:
  - Windows 10 (Brasco - client)
  - Windows Server 2019 (BigGuy - print target + WSL host)
  - Debian 12 (ABC Server - native CUPS print server)
  - Linux Mint (ABC Client - client)
- All VMs on the same virtual network

## Step 1: Install CUPS and CUPS-PDF on Debian 12 (ABC Server)
sudo apt update
sudo apt install cups cups-pdf -y
sudo systemctl enable --now cups

## Step 2: Configure CUPS for Remote Access and Sharing (Debian & WSL)
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

Restart CUPS after editing:
sudo systemctl restart cups

## Step 3: Add CUPS-PDF Virtual Printer (Debian & WSL)
Open browser to http://<server-ip>:631 (or localhost:631 in WSL)
Administration → Add Printer → CUPS-PDF backend
Set name and location → Share the printer

Recommended names:
- DebianPDF (on Debian ABC Server)
- WindowsServerPDF (in WSL on BigGuy Windows Server)

## Step 4: Configure PDF Output to Windows Filesystem (cups-pdf.conf)
Edit /etc/cups/cups-pdf.conf on both CUPS instances (Debian and WSL):
Out /mnt/c/Users/Public/Desktop/PrintedDocs/

Create the folder on the Windows host:
C:\Users\Public\Desktop\PrintedDocs (create if missing)

## Step 5: Install WSL + Ubuntu on Windows Server 2019 (BigGuy)
On Windows Server 2019:
wsl --install -d Ubuntu

Launch Ubuntu in WSL and repeat Steps 1–3 (install CUPS, configure cupsd.conf, add CUPS-PDF printer).

## Step 6: Deploy Flask PDF Upload Portal (in WSL on Windows 10 or Server)
In WSL:
sudo apt install python3-pip -y
pip install flask
mkdir flask-app && cd flask-app

Create app.py — full source code: [flask-app/app.py](../flask-app/app.py)

Run the app:
python3 app.py

Access from Windows browser: http://<wsl-ip>:5000
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
- Upload PDF from Windows 10 via Flask portal → check CUPS job queue[](http://<server-ip>:631) and output folder (PrintedDocs)
- Print test page from Linux Mint to both printers → confirm PDF appears in PrintedDocs folder
- View all jobs and status at http://<server-ip>:631

## Additional Notes
- Firewall: Allow port 631 (CUPS) and 5000 (Flask)
  Debian/WSL: sudo ufw allow 631
  Windows firewall: allow inbound 631 and 5000
- Troubleshooting: Check CUPS error log (/var/log/cups/error_log) if jobs fail
- No Samba used — all sharing via HTTP/IPP

See full original proposal PDF: [BigGuy Corp Multi-access Print Services Proposal](../docs/BigGuy-Corp-Print-Services-Proposal.pdf) (upload the PDF to docs/ folder if not already done)
