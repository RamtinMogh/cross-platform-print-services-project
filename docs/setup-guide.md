# Setup Guide – Cross-Platform Print Services

This document outlines the setup process used to implement
multi-access print services across Windows and Linux systems in a
virtualized lab environment.

The goal was to enable reliable PDF-based printing between BigGuy Corp,
ABC Co., and Brasco workstations using open-source tools.

---

## Environment Overview
- Windows Server 2019 (BigGuy)
- Debian Linux (ABC Server)
- Linux Mint (ABC Client)
- Windows 10 (Brasco)
- WSL (Ubuntu) running on Windows 10
- VMware used for virtualization

---

## Step 1: Configure CUPS Print Services
CUPS was installed and configured on Debian Linux and within WSL to act
as the primary print service.

Key actions:
- Installed CUPS and CUPS-PDF
- Enabled remote access and printer sharing over HTTP (IPP)
- Verified access to the CUPS web interface (port 631)

PDF printers were used for testing to avoid dependency on physical
hardware.

---

## Step 2: Enable Cross-System Printing
Printers hosted on Linux systems were shared using CUPS over HTTP,
allowing other systems to submit print jobs using IPP URLs.

This approach avoided Samba-based printer sharing due to compatibility
issues between Windows and Linux systems.

---

## Step 3: Windows-to-CUPS Printing via WSL
Because Windows could not reliably discover CUPS printers hosted inside
WSL, a workaround was implemented.

Key actions:
- Installed Ubuntu under WSL on Windows 10
- Configured CUPS within WSL
- Used Linux print tools (`lp`) to submit print jobs

---

## Step 4: Flask PDF Upload Interface
A Flask-based web application was developed to allow users on Windows 10
to upload PDF files for printing.

Workflow:
- User uploads a PDF via a web interface
- The file is passed to WSL
- CUPS processes the print job using a PDF printer

This enabled manual printing from Windows without relying on native
printer discovery.

---

## Step 5: Output Handling and Verification
Printed PDF files were automatically moved from the WSL filesystem into
the Windows filesystem using shell scripting.

This allowed centralized access to print output and simplified
verification during testing.

---

## Validation
- Print jobs were successfully submitted from Windows and Linux systems
- Output PDFs were generated consistently
- The solution was demonstrated live in a VMware lab environment

