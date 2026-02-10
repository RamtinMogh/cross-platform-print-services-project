# Problem Statement

**Project Context**  
This solution was developed for a simulated enterprise scenario (BigGuy Corp) requiring reliable cross-platform printing in a mixed Windows and Linux environment. The original assignment involved a group, but I personally designed, implemented, configured, and documented the complete architecture.

**Core Requirements**  
- Enable two-way printing:  
  - Windows 10 client (Brasco) submits print jobs to:  
    - Debian CUPS-PDF server (ABC Server)  
    - Windows Server 2019 printer/share (BigGuy)  
  - Linux Mint client (ABC Client) prints natively to both targets  
- Eliminate Samba dependency due to repeated compatibility failures  
- Use only open-source, zero-cost tools (no proprietary software or hardware upgrades)  
- Minimize changes to existing infrastructure  

**Key Challenge**  
Direct printing from Windows 10 to Linux-based CUPS printers was unreliable (discovery and compatibility issues). A practical workaround was needed to bridge the platforms without introducing paid solutions.

**Objective**  
Deliver a flexible, scalable, bidirectional printing system using CUPS over HTTP/IPP, WSL bridging, a custom Flask PDF upload portal, and Bash automation — all while keeping the solution fully open-source and cost-free.
