# Lancer v0.0.2 Alpha

## Badges & Statuses

|Branch|Status|Coverage|Code Quality|Last Commit|
|---|---|---|---|---|
|Master|[![Build Status](https://travis-ci.com/Stormy102/Lancer.svg?branch=master)](https://travis-ci.com/Stormy102/Lancer) |[![Coverage Status](https://coveralls.io/repos/github/Stormy102/Lancer/badge.svg)](https://coveralls.io/github/Stormy102/Lancer)|[![Master Code Quality](https://codebeat.co/badges/08113589-61c1-418c-8f2e-bffcc5562425)](https://codebeat.co/projects/github-com-stormy102-lancer-master)|[![Last Master Commit](https://img.shields.io/github/last-commit/Stormy102/Lancer.svg)]()
|Develop|[![Develop Build Status](https://travis-ci.com/Stormy102/Lancer.svg?branch=develop)](https://travis-ci.com/Stormy102/Lancer)|[![Coverage Status](https://coveralls.io/repos/github/Stormy102/Lancer/badge.svg?branch=develop)](https://coveralls.io/github/Stormy102/Lancer?branch=develop)|[![Develop Code Quality](https://codebeat.co/badges/10ed4785-93e2-47ad-8504-827f22c74aa1.svg)](https://codebeat.co/projects/github-com-stormy102-lancer-develop)|[![Last Develop Commit](https://img.shields.io/github/last-commit/Stormy102/Lancer/develop.svg)]()|

<!--- See for dropping Python 3.5 support https://devguide.python.org/#status-of-python-branches -->
[![Python Versions](https://img.shields.io/badge/python-3.5|3.6|3.7|3.8-blue.svg)]()
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Releases](https://img.shields.io/github/v/release/Stormy102/Lancer?include_prereleases)]()
[![Maintenance](https://img.shields.io/maintenance/yes/2019.svg)]()
[![Known Vulnerabilities](https://snyk.io//test/github/Stormy102/Lancer/badge.svg?targetFile=requirements.txt)](https://snyk.io//test/github/Stormy102/Lancer?targetFile=requirements.txt)
[![Contributors](https://img.shields.io/github/contributors/Stormy102/Lancer.svg)]()
[![Issues](https://img.shields.io/github/issues/Stormy102/Lancer.svg)](https://github.com/Stormy102/Lancer/issues)

## What is this?

Lancer is a pentesting tool written in [Python 3](https://www.python.org/) which aims in automating and expediating recon and vulnerability scanning.

## Sigh... Another pentesting tool? Why should I use this?

The aim of Lancer is to take several tools which already exist, such as [Gobuster](https://github.com/OJ/gobuster/), [Nmap](https://github.com/nmap/nmap), [SMBMap](https://github.com/ShawnDEvans/smbmap) and [many](https://github.com/portcullislabs/enum4linux) [more](https://github.com/sullo/nikto), and intelligently detect which tools should be used depending on the results of a scan. This is meant to automate enumeration of a target and make the process of finding vulnerabilities a bit easier.

## Installation

To execute the program, ensure that you have Python 3.5 or higher installed. Use Python's pip to install the necessary Python dependents
```shell script
pip install -r requirements.txt
```
---
However, Lancer depends on several other external programs being installed. For each of these programs, the environmental PATH variable must point to them so that they can be executed by Python.

|Program|Version|Required|Optional|Linux|Windows|
|---|---|---|---|---|---|
|[Nmap](https://github.com/nmap/nmap)|7.7.0|✔| |✔|✔|
|[Gobuster](https://github.com/OJ/gobuster/releases)|3.1| |✔*|✔|✔|
|[Smbmap](https://github.com/ShawnDEvans/smbmap)|b55fc05| |✔*|✔|✔|
|[Nikto](https://github.com/sullo/nikto)|2.1.6| |✔|✔|✔|
|[enum4linux](https://github.com/portcullislabs/enum4linux)|0.8.9| |✔|✔|❌|

*Recommended program

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

See the config.ini file for more options C:\Users\Matthew\.lancer\config.ini

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

## Limitations & Upcoming Features

As Lancer is still very much in active development, there is currently limited functionality. This is a list of 
features which we intend to add support for.
* ~~Nmap scanning~~ _Added in 0.0.1_
* ~~Gobuster enumeration~~ _Added in 0.0.1_
* ~~Searchsploit Nmap results~~ _Added in 0.0.1_
* FTP scanning/downloading files < 50mb _In Development - Planned for 0.0.2_
* SMB enumeration _Planned for 0.0.2_
* Limited target attacks. Scans and enumerates specific services only _Planned for 0.0.3_
* Further services detection _Coming soon_
    * SQL
    * SSH
    * Telnet
    * SMTP
    * DNS
    * POP3
    * RCPBind
    * MSRPC
    * IMAP
    * HTTPS
    * VNC
	* RDP
* enum4linux support _Coming soon_
* Multi-language support _Coming soon_

Any other features you want to see? Open a Github Issue or a pull request

## License

GPL-3.0. See the LICENSE file for more details.