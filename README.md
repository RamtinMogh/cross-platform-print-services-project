# Cross-Platform Print Services (CUPS + WSL + Flask)

**Two-way printing bridge for hybrid Windows/Linux environments** — Enables reliable print jobs between Windows 10 clients, Windows Server 2019, Debian CUPS servers, and Linux Mint clients using only open-source tools. Built as a Seneca College group project to eliminate Samba compatibility issues.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-orange?logo=flask)](https://flask.palletsprojects.com/)
[![CUPS](https://img.shields.io/badge/CUPS-2.x-green)](https://www.cups.org/)
[![WSL](https://img.shields.io/badge/WSL-Ubuntu-blue?logo=linux)](https://learn.microsoft.com/en-us/windows/wsl/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview
This project delivers a cost-free, open-source cross-platform printing solution for a mixed-OS enterprise environment (BigGuy Corp simulation):

- **Brasco** (Windows 10 client) submits print jobs to **ABC Server** (Debian CUPS-PDF) and **BigGuy** (Windows Server 2019)
- **ABC Client** (Linux Mint) prints natively to both targets
- Custom **Flask web portal** (running in WSL) allows Windows users to upload PDFs and submit to CUPS when native discovery fails
- Printed PDFs automatically move from WSL filesystem to Windows host (e.g., Public Desktop)

Core workaround: Bridge Windows → CUPS limitations using WSL + HTTP/IPP sharing + Flask upload → `lp` submission.

Full project proposal (excerpts): [BigGuy Corp Multi-access Print Services Proposal](./docs/proposal_excerpts.md) or attach the PDF if you upload it.

## Goals
- Enable bidirectional printing in hybrid Windows/Linux setups
- Avoid proprietary tools or Samba dependencies
- Use open-source components only (CUPS, IPP/HTTP, WSL, Flask, Bash)
- Demonstrate practical troubleshooting in a virtualized lab

## Technologies Used
- CUPS / CUPS-PDF (printer management & virtual PDF output)
- WSL (Ubuntu on Windows host)
- Flask (Python) – web upload portal
- Bash scripting – post-print file relocation
- IPP/HTTP printing (CUPS shared over port 631)
- VMware Workstation – multi-OS virtual lab

## What I Built / Contributed
- Configured CUPS on Debian (native) and WSL (Ubuntu) with HTTP sharing, security hardening (`cupsd.conf`, `cups-pdf.conf`)
- Developed Flask upload interface to submit PDFs via `lp` command
- Created Bash automation script to relocate printed PDFs from WSL to Windows filesystem
- Documented complete setup, configs, and troubleshooting (DNS, auth, file trapping issues)

## Setup Guide
Detailed steps in [`docs/setup-guide.md`](./docs/setup-guide.md).

Quick summary:
1. Deploy VMs in VMware (Windows 10, Windows Server 2019 + WSL, Debian 12, Linux Mint)
2. Install/configure CUPS + CUPS-PDF on servers; share printers over HTTP
3. Run Flask app in WSL: `python app.py`
4. Access upload portal[](http://<wsl-ip>:5000) from Windows to submit PDFs

## Results
- Achieved consistent two-way printing without Samba
- Fully functional in VMware virtual lab environment
- Zero-cost, scalable solution using open-source tools

## Representative Illustrations
Representative examples of key components (generic/public images matching the setup):

- **CUPS Web Administration Interface** (printer management and sharing config)

<grok-card data-id="09068b" data-type="image_card" data-plain-type="render_searched_image"  data-arg-size="LARGE" ></grok-card>



<grok-card data-id="dda47a" data-type="image_card" data-plain-type="render_searched_image"  data-arg-size="LARGE" ></grok-card>


- **Flask PDF Upload Portal** (custom web interface for Windows clients)

<grok-card data-id="f619b2" data-type="image_card" data-plain-type="render_searched_image"  data-arg-size="LARGE" ></grok-card>


- **Hybrid Virtualization Architecture** (VMware lab with Windows/Linux VMs)

<grok-card data-id="5cb071" data-type="image_card" data-plain-type="render_searched_image"  data-arg-size="LARGE" ></grok-card>



<grok-card data-id="f12fe4" data-type="image_card" data-plain-type="render_searched_image"  data-arg-size="LARGE" ></grok-card>


(You can replace these later with your own recreated screenshots if you spin up the lab again — e.g., actual CUPS page, your Flask form, output folder.)

## Challenges & Resolutions
- Samba/CUPS incompatibility → Switched to WSL + CUPS-PDF bridge
- No native Windows discovery of CUPS printers → Built Flask portal workaround
- PDFs trapped in WSL filesystem → cups-pdf.conf Out directive + Bash mover script

## Repository Structure
- `docs/` → Setup guide, problem statement, configs
- `flask-app/` → Flask source (app.py, templates/)
- `scripts/` → Bash automation (PDF handler)
- `diagrams/` → Architecture diagrams (add your own if possible)

Feel free to fork/contribute!
