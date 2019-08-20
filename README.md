# Lancer v0.0.1a1

## Tags, Statuses, etc

[![Build Status](https://travis-ci.com/Stormy102/Lancer.svg?branch=master)](https://travis-ci.com/Stormy102/Lancer) 
[![Develop Build Status](https://travis-ci.com/Stormy102/Lancer.svg?branch=develop)](https://travis-ci.com/Stormy102/Lancer)
[![Issues](https://img.shields.io/github/issues/Stormy102/Lancer)](https://github.com/Stormy102/Lancer/issues)
[![Licence](https://img.shields.io/github/license/Stormy102/Lancer)]()
[![Contributors](https://img.shields.io/github/contributors/Stormy102/Lancer)]()
[![Last Commit](https://img.shields.io/github/last-commit/Stormy102/Lancer)]()
[![Last Commit](https://img.shields.io/maintenance/yes/2019)]()

## What is this?

Lancer is a pentesting tool written in [Python 3](https://www.python.org/) which aims in automating and expediating recon and vulnerability scanning.

## Sigh... Another pentesting tool? Why should I use this?

The aim of Lancer is to take several tools which already exist, such as [Gobuster](https://github.com/OJ/gobuster/), [Nmap](https://github.com/nmap/nmap), [SMBMap](https://github.com/ShawnDEvans/smbmap) and [many](https://github.com/portcullislabs/enum4linux) [more](https://github.com/sullo/nikto), and intelligently detect which tools should be used depending on the results of a scan. This is meant to automate enumeration of a target and make the process of finding vulnerabilities a bit easier.

## Usage

```text
usage: lancer.py [-h] (-T TARGET | --target-file FILE) [-q] [-v] [-sd]
                 [--skip-ports PORTS [PORTS ...]] [--show-output]
                 [--nmap FILE] [-wW WORDLIST] [-fD DOMAIN] [-fU USERNAME]
                 [-fP PASSWORD]

Lancer - system vulnerability scanner

This tool is designed to aid the recon phase of a pentest or any legal & authorised attack against a device or network. The author does not take any liability for use of this tool for illegal use.

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
  --skip-ports PORTS [PORTS ...]
                        Set the ports to ignore. These ports will have no
                        enumeration taken against them, except for the initial
                        discovery via nmap. This can be used to run a custom
                        scan and pass the results to Lancer.
  --show-output         Show the output of the programs which are executed,
                        such as nmap, nikto, smbclient and gobuster
  --nmap FILE           Skip an internal nmap scan by providing the path to an
                        nmap XML file

Web Services:
  Options for targeting web services

  -wW WORDLIST          The wordlist to use. Defaults to the
                        directory-2.3-medium.txt file found in
                        /usr/share/wordlists/dirbuster

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
## License

See the LICENSE file. 