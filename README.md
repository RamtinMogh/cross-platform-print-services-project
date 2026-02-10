# Cross-Platform Print Services (CUPS + WSL + Flask)

**Two-way printing bridge for hybrid Windows/Linux environments** — Enables reliable bidirectional print jobs between Windows 10 clients, Windows Server 2019, Debian CUPS servers, and Linux Mint clients using only open-source tools. No Samba required.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-orange?logo=flask)](https://flask.palletsprojects.com/)
[![CUPS](https://img.shields.io/badge/CUPS-2.x-green)](https://www.cups.org/)
[![WSL](https://img.shields.io/badge/WSL-Ubuntu-blue?logo=linux)](https://learn.microsoft.com/en-us/windows/wsl/)

## Overview
Built for a simulated enterprise (BigGuy Corp) with mixed OSes:
- Windows 10 client (Brasco) submits print jobs to Debian CUPS-PDF (ABC Server) and Windows Server 2019 (BigGuy)
- Linux Mint client (ABC Client) prints natively to both targets

Key challenge solved: Native Windows discovery of CUPS printers inside WSL is unreliable → created a **Flask web portal** running in WSL for PDF uploads → submitted via `lp` to CUPS.

Printed PDFs auto-relocated from WSL filesystem to Windows host (e.g., Public Desktop) for easy access.

All tools open-source and zero-cost: CUPS, WSL (Ubuntu), Flask, Bash.

## Goals
- Enable reliable two-way printing in hybrid Windows/Linux setups
- Eliminate Samba dependency and compatibility issues
- Use only open-source components
- Demonstrate practical systems administration and troubleshooting in a virtual lab

## Technologies Used
- CUPS / CUPS-PDF (printer server & virtual PDF printer)
- WSL (Ubuntu on Windows Server 2019 host)
- Flask (Python) – custom PDF upload web interface
- Bash scripting – automated PDF file relocation
- IPP/HTTP printing (CUPS shared over port 631)
- VMware Workstation – multi-VM lab environment (Windows 10, Windows Server 2019 + WSL, Debian 12, Linux Mint)

## What I Implemented
- Configured CUPS on native Debian 12 and inside WSL (Ubuntu) with HTTP/IPP sharing
- Hardened CUPS configs (`cupsd.conf` for remote access, `cups-pdf.conf` for output path to Windows filesystem)
- Built Flask web app (`flask-app/`) with file upload form → selects printer → submits via `lp` command
- Wrote Bash post-processing script (`scripts/move_pdfs.sh`) to move printed PDFs from WSL to host Windows folder
- Resolved real issues: WSL printer invisibility in Windows dialog, PDFs trapped in Linux filesystem, CUPS web UI limitations for uploads
- Documented full setup, configs, and troubleshooting steps

## Setup Guide
See detailed instructions in [`docs/setup-guide.md`](./docs/setup-guide.md).

Quick high-level steps:
1. Create VMs in VMware: Windows 10 (client), Windows Server 2019 (with WSL Ubuntu), Debian 12 (CUPS server), Linux Mint (client)
2. Install CUPS + CUPS-PDF on Debian and WSL; configure sharing over HTTP
3. Set up printer queues (e.g., DebianPDF, WindowsServerPDF)
4. Deploy and run Flask app in WSL
5. From Windows 10: access Flask portal → upload PDF → select printer → print
6. Verify output PDFs appear on Windows filesystem

## Results
- Consistent bidirectional printing achieved across all four OS combinations
- No reliance on Samba or proprietary software
- Fully functional in virtualized lab environment
- Practical demonstration of hybrid systems integration, scripting, and workaround design

## Challenges & Resolutions
- Samba/CUPS incompatibility in mixed environments → Used WSL + CUPS-PDF bridge
- Windows cannot natively discover CUPS printers in WSL → Built custom Flask upload portal
- Printed files trapped inside WSL → Modified `cups-pdf.conf` Out directive + Bash script to relocate to `/mnt/c/...`

## Repository Structure
- `docs/`          → Problem statement, detailed setup guide, config excerpts
- `flask-app/`     → Flask application source (app.py, templates/, static/ if any)
- `scripts/`       → Bash automation scripts (e.g., PDF mover)

This repo showcases my hands-on experience with Linux/Windows integration, CUPS administration, web scripting for IT workarounds, and virtualization troubleshooting.
