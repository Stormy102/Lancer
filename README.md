# Lancer v0.0.3 Alpha

<p align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#usage">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a>
</p>

|Branch|Status|Coverage|Code Quality|Last Commit|
|---|---|---|---|---|
|Master|[![Build Status](https://travis-ci.com/Stormy102/Lancer.svg?branch=master)](https://travis-ci.com/Stormy102/Lancer) |[![Coverage Status](https://coveralls.io/repos/github/Stormy102/Lancer/badge.svg)](https://coveralls.io/github/Stormy102/Lancer)|[![Master Code Quality](https://codebeat.co/badges/08113589-61c1-418c-8f2e-bffcc5562425)](https://codebeat.co/projects/github-com-stormy102-lancer-master)|[![Last Master Commit](https://img.shields.io/github/last-commit/Stormy102/Lancer.svg)]()
|Develop|[![Develop Build Status](https://travis-ci.com/Stormy102/Lancer.svg?branch=develop)](https://travis-ci.com/Stormy102/Lancer)|[![Coverage Status](https://coveralls.io/repos/github/Stormy102/Lancer/badge.svg?branch=develop)](https://coveralls.io/github/Stormy102/Lancer?branch=develop)|[![Develop Code Quality](https://codebeat.co/badges/10ed4785-93e2-47ad-8504-827f22c74aa1.svg)](https://codebeat.co/projects/github-com-stormy102-lancer-develop)|[![Last Develop Commit](https://img.shields.io/github/last-commit/Stormy102/Lancer/develop.svg)]()|

<!--- See for dropping Python 3.5 support https://devguide.python.org/#status-of-python-branches -->
[![Python Versions](https://img.shields.io/badge/python-3.5|3.6|3.7|3.8-blue.svg)]()
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Status](https://img.shields.io/badge/status-Pre%20Release-red.svg)]()
[![Releases](https://img.shields.io/github/v/release/Stormy102/Lancer?include_prereleases)]()
[![Maintenance](https://img.shields.io/maintenance/yes/2019.svg)]()
[![Known Vulnerabilities](https://snyk.io//test/github/Stormy102/Lancer/badge.svg?targetFile=requirements.txt)](https://snyk.io//test/github/Stormy102/Lancer?targetFile=requirements.txt)
[![Contributors](https://img.shields.io/github/contributors/Stormy102/Lancer.svg)]()
[![Issues](https://img.shields.io/github/issues/Stormy102/Lancer.svg)](https://github.com/Stormy102/Lancer/issues)

## Introduction

### What is this?

Lancer is a pentesting tool written in [Python 3](https://www.python.org/) which aims in automating and expediating recon and vulnerability scanning.

### Sigh... Another pentesting tool? Why should I use this?

The aim of Lancer is to take several tools which already exist, such as [Gobuster](https://github.com/OJ/gobuster/), [Nmap](https://github.com/nmap/nmap), [SMBMap](https://github.com/ShawnDEvans/smbmap) and [many](https://github.com/portcullislabs/enum4linux) [more](https://github.com/sullo/nikto), and intelligently detect which tools should be used depending on the results of a scan. This is meant to automate enumeration of a target and make the process of finding vulnerabilities a bit easier.

## Limitations & Upcoming Features

As Lancer is still very much in active development, there is currently limited functionality and it is not recommended for use in a commercial or real-world environment.

This is a list of features which we intend to add support for:
* ~~Nmap scanning~~ _Added in 0.0.1_
* ~~Gobuster enumeration~~ _Added in 0.0.1_
* ~~Searchsploit Nmap results~~ _Added in 0.0.1_
* ~~Configuration file (.ini) for persistent configuration~~ _Added on develop branch for 0.0.2_
* ~~FTP scanning/downloading files < 50mb~~ _Added in 0.0.2_
* ~~Nikto support~~ _Added in 0.0.2_
* ~~HTTPS support - certificate extraction, normal HTTP services scanning and enumeration~~ _Added in 0.0.3_
* ~~Multiple targets from file support~~ _Added in 0.0.3_
* ~~Convert domain name to IP~~ _Added in 0.0.3_
* Write all output to file via -o parameter _Planned for 0.0.3_
* SSH support - display fingerprint and SSH version _Planned for 0.0.3_
* Limited target attacks. Scans and enumerates specific services only _Planned for 0.0.4_
* SMB enumeration with SMBClient/smbmap _Planned for 0.0.4_
* Multi-threading - run all components at the same time, with progress indicator `[!] 3/7 scans complete... /` _Planned for 0.0.4_
* Multi-language support _Planned for 0.0.5_
* Nmap script level _Planned for 0.0.5_
* enum4linux support _Planned for 0.0.5_
* WPScan support _Planned for 0.0.6_
* Metasploit RPC support _Coming soon_
* Further services detection _Coming soon_
    * SQL
    * Telnet
    * SMTP
    * DNS
    * POP3
    * RCPBind
    * MSRPC
    * IMAP
    * VNC
	* RDP
	* Active Directory
* Further software which may be implemented upon evaluation:
    * Amap
    * arp-scan
    * dnsenum/dnsmap/dnsrecon
    * dotdotpawn
    * eyewitness
    * ident (port 113)
    * iSMTP/smtp-user-enum
    * lbd
    * Miranda
    * p0f
    * parsero
    * WOL-E
    * doona
    * SidGuesser
    * sqlmap
    * sqlninja/sqlsus
    * WhatWeb

Any other features you want to see? Open a Github Issue or a pull request

## Installation

To get started with Lancer, either download the zip from Github with Clone or Download > Download Zip or `git clone https://github.com/Stormy102/Lancer`

Lancer is tested and supported on the following Operating Systems:
  * Windows:
    * Windows 7
    * Windows 8/8.1/8.1.1
    * Windows 10 (all versions)
  * Linux:
    * Ubuntu 16.04 and up
    * Debian 8 and up


To execute the program, ensure that you have Python 3.5 or higher installed. Use Python's pip to install the necessary Python dependencies.
```shell script
pip install -r requirements.txt
```
---
However, Lancer has dependencies on several other external programs being installed. For each of these programs, the environmental PATH variable must point to them so that they can be executed by Python.

|Program|Version|Required|Optional|Linux|Windows|
|---|---|---|---|---|---|
|[Nmap](https://github.com/nmap/nmap)|7.7.0|✔| |✔|✔|
|[Gobuster](https://github.com/OJ/gobuster/releases)|3.1| |✔*|✔|✔|
|[Searchsploit](https://github.com/offensive-security/exploitdb/blob/master/searchsploit)|cbf80e3| |✔*|✔|❌|
|[Smbmap](https://github.com/ShawnDEvans/smbmap)|b55fc05| |✔*|✔|✔|
|[Nikto](https://github.com/sullo/nikto)|2.1.6| |✔|✔|✔|
|[enum4linux](https://github.com/portcullislabs/enum4linux)|0.8.9| |✔|✔|❌|

*_Recommended program_

## Usage

The program takes the following arguments:

```text
usage: lancer.py [-h] (-T TARGET | --target-file FILE) [-q] [-v] [-sd]
                 [--cache-root PATH] [--skip-ports PORTS [PORTS ...]]
                 [--show-output] [-l LANGUAGE] [--nmap FILE] [--udp]
                 [-wW WORDLIST] [--web-scan-only] [-fD DOMAIN] [-fU USERNAME]
                 [-fP PASSWORD]

Lancer - system vulnerability scanner

This tool is designed to aid the recon phase of a pentest or any legal & authorised attack against a device or network. The author does not take any liability for use of this tool for illegal use.

See the config.ini file for more options ~\.lancer\config.ini

optional arguments:
  -h, --help            show this help message and exit

Main arguments:
  -T TARGET, --target TARGET
                        IP of target
  --target-file FILE    File containing a list of target IP addresses
  -q, --quiet           Do a quiet nmap scan. This will help reduce the
                        footprint of the scan in logs and on IDS which may be
                        present in a network.
  -v, --verbose         Use a more verbose output. This will output more
                        detailed information and may help to diagnose any
                        issues
  -sd, --skip-disclaimer
                        Skip the legal disclaimer. By using this flag, you
                        agree to use the program for legal and authorised use
  --cache-root PATH     The root of the cache. This is where all of the data
                        for the programs run is stored, which may be useful if
                        you wish to document or save all of the data cleanly.
  --skip-ports PORTS [PORTS ...]
                        Set the ports to ignore. These ports will have no
                        enumeration taken against them, except for the initial
                        discovery via nmap. This can be used to run a custom
                        scan and pass the results to Lancer.
  --show-output         Show the output of the programs which are executed,
                        such as nmap, nikto, smbclient and gobuster
  -l LANGUAGE, --language LANGUAGE
                        Language you want Lancer to run in. Defaults to
                        English !!NOT YET IMPLEMENTED!!
  --nmap FILE           Skip an internal nmap scan by providing the path to an
                        nmap XML file
  --udp                 Scan for UDP ports as well as TCP when using nmap.
                        This will look for more ports but will result in a
                        much longer scan time

Web Services:
  Options for targeting web services

  -wW WORDLIST, --web-wordlist WORDLIST
                        The wordlist to use. The default wordlist can be
                        changed in the config file
  --web-scan-only       Perform a web scan only. This runs a custom Nmap scan
                        on ports 80, 443, 3000 and 8080, and runs the web
                        modules against that target. NOT YET IMPLEMENTED

File Services:
  Options for targeting file services

  -fD DOMAIN            Domain to use during the enumeration of file services
  -fU USERNAME          Username to use during the enumeration of file
                        services
  -fP PASSWORD          Password to use during the enumeration of file
                        services

Examples:

$ python lancer.py -T 10.10.10.100 --verbose
$ python lancer.py --target-file targets --skip-ports 445 8080 --show-program-output
$ python lancer.py --target 192.168.1.10 --nmap nmap/bastion.xml /
  -wW /usr/share/wordlists/dirbuster/directory-2.3-small.txt /
  -fD HTB -fU L4mpje -fP P@ssw0rd
```

## Contributing

Thanks for your interest in contributing to this project. You can contribute or report issues in the following ways:

### Pull Requests
If you would like to create a pull request, please make sure that you are on the [develop branch](https://github.com/Stormy102/Lancer/tree/develop) before opening one. Once you have cloned or forked this repo, open the root of the cloned repo to begin development. This project uses [git-flow](https://github.com/nvie/gitflow) as its branching model.

The current development environment is with [PyCharm](https://www.jetbrains.com/pycharm/). Please make sure you are using these versions before submitting any pull requests.

#### Coding Conventions
This project uses [Pep8](https://www.python.org/dev/peps/pep-0008/) to maintain a consistent coding style. PyCharm uses the Pep8 style, which makes conformity easier.  

### Reporting bugs
If you find a bug, crash or any other intende

## Credits

See [Credits.md](CREDITS.MD) for the credits

## License

GPL-3.0. See the [LICENSE](LICENCE) file for more details.