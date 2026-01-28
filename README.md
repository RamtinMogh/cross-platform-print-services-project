# cross-platform-print-services-project
Cross-platform print services using CUPS + WSL with a Flask PDF upload interface for Windows-to-CUPS printing.

# Cross-Platform Print Services (CUPS + WSL + Flask)

## Overview
This project implements a cross-platform printing solution across a virtual lab environment, enabling print workflows between:
- Windows 10 client
- Windows Server (print target / services)
- Debian Linux print server
- Linux Mint client

The solution uses **CUPS** for printer management and sharing over **HTTP/IPP**, and **WSL (Ubuntu)** to support Linux-based tooling from a Windows environment. A **Flask upload portal** was used to submit PDF print jobs into WSL/CUPS when direct printer discovery was not reliable.

See [`docs/problem-statement.md`](docs/problem-statement.md) for the original requirements and constraints.

## Goals
- Enable printing across mixed Windows + Linux systems
- Maintain compatibility using open-source tools (CUPS/IPP)
- Provide a practical workaround for Windows-to-CUPS printing via WSL

## Technologies Used
- CUPS / CUPS-PDF
- WSL (Ubuntu)
- Flask (Python)
- Bash scripting
- IPP/HTTP printing (CUPS over port 631)
- VMware (virtualized lab environment)

## What I Built / Implemented
- Configured CUPS and printer sharing over HTTP/IPP
- Set up printing from Windows through WSL into CUPS
- Built a Flask web interface to upload PDFs and submit print jobs
- Automated handling of printed PDF output to the Windows filesystem

## Results
- Achieved consistent cross-platform printing behavior without relying on Samba printer sharing
- Demonstrated multi-OS printing workflows in a VMware lab environment

## Screenshots
This project was demonstrated live in a VMware lab environment during class.
Screenshots were not captured at the time. Configuration notes and scripts are provided to demonstrate implementation.

## Repository Contents (Coming Next)
- `docs/` setup notes and troubleshooting
- `flask-app/` Flask upload portal source
- `scripts/` automation scripts (PDF handling)
- `diagrams/` architecture diagram
