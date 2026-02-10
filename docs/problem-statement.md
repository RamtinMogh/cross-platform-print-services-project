# Problem Statement

BigGuy Corp needed reliable cross-platform printing in a mixed Windows + Linux environment after upgrading systems.

Requirements:
- Windows 10 client (Brasco) must print to both Debian CUPS-PDF (ABC Server) and Windows Server 2019 (BigGuy)
- Linux Mint client (ABC Client) must print to both targets
- No Samba (due to repeated compatibility failures)
- No proprietary software or new hardware purchases
- Minimal changes to existing infrastructure

Goal: Build a stable, cost-free workaround using only open-source tools (CUPS, WSL, Flask, Bash).
