# Setup Guide - Cross-Platform Print Services

This guide lists the steps I followed in a VMware lab to set up the cross-platform printing solution.

## Lab Environment
- Hypervisor: VMware Workstation
- VMs:
  - Windows 10 (client - Brasco)
  - Windows Server 2019 (print target + WSL host - BigGuy)
  - Debian 12 (CUPS print server - ABC Server)
  - Linux Mint (client - ABC Client)
- All VMs on the same virtual network

## Step 1: CUPS on Debian 12 (ABC Server)
Run these commands:
sudo apt update
sudo apt install cups cups-pdf -y
sudo systemctl enable --now cups

Edit /etc/cups/cupsd.conf:
- Change Listen localhost:631 to Listen 0.0.0.0:631
- In <Location /> and <Location /admin>:
  Order allow,deny
  Allow all
- Add: WebInterface Yes
- Add: Browsing On

Restart CUPS:
sudo systemctl restart cups

Add PDF printer:
- Go to http://<debian-ip>:631
- Administration > Add Printer > CUPS-PDF
- Name it: DebianPDF

## Step 2: CUPS in WSL on Windows Server 2019 (BigGuy)
On Windows Server 2019:
- Enable WSL and install Ubuntu

In WSL:
sudo apt update && sudo apt install cups cups-pdf -y
sudo systemctl enable --now cups

Apply same cupsd.conf changes as Step 1 (use sudo nano /etc/cups/cupsd.conf)

Add PDF printer:
- Go to http://localhost:631 (or network IP)
- Add CUPS-PDF
- Name it: WindowsServerPDF

## Step 3: PDF Output to Windows Folder
Edit /etc/cups/cups-pdf.conf (both servers):
Out /mnt/c/Users/Public/Desktop/PrintedDocs/

Create folder on Windows:
C:\Users\Public\Desktop\PrintedDocs

## Step 4: Flask PDF Upload Portal (in WSL)
In WSL:
sudo apt install python3-pip -y
pip install flask
mkdir flask-app && cd flask-app

Create app.py (code is in flask-app/app.py in this repo)

Run:
python3 app.py

Access from Windows browser:
http://<wsl-ip>:5000
Upload PDF, choose printer (DebianPDF or WindowsServerPDF), submit

## Step 5: Printing from Linux Mint
On Linux Mint:
- Settings > Printers > Add Printer
- Use IPP: ipp://<server-ip>:631/printers/DebianPDF

## Verification
- From Windows: upload PDF via Flask → check CUPS queue + output folder
- From Linux Mint: print test page → confirm output on both targets
- View jobs: http://<server-ip>:631

Notes:
- May need: ufw allow 631 on Debian
- Allow ports 631 and 5000 in Windows firewall if blocked
