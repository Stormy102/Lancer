# Lancer v0.0.3 Alpha

![Lancer in action](.github/images/lancer-header.png)

<p align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#limitations--upcoming-features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a>
</p>

|Branch|Status|Coverage|Code Quality|Last Commit|
|---|---|---|---|---|
|Master|[![Build Status](https://travis-ci.com/Stormy102/Lancer.svg?branch=master)](https://travis-ci.com/Stormy102/Lancer) |[![Coverage Status](https://coveralls.io/repos/github/Stormy102/Lancer/badge.svg)](https://coveralls.io/github/Stormy102/Lancer)|[![Master Code Quality](https://codebeat.co/badges/08113589-61c1-418c-8f2e-bffcc5562425)](https://codebeat.co/projects/github-com-stormy102-lancer-master)|[![Last Master Commit](https://img.shields.io/github/last-commit/Stormy102/Lancer.svg)](https://github.com/Stormy102/Lancer/commits/master)
|Develop|[![Develop Build Status](https://travis-ci.com/Stormy102/Lancer.svg?branch=develop)](https://travis-ci.com/Stormy102/Lancer)|[![Coverage Status](https://coveralls.io/repos/github/Stormy102/Lancer/badge.svg?branch=develop)](https://coveralls.io/github/Stormy102/Lancer?branch=develop)|[![Develop Code Quality](https://codebeat.co/badges/10ed4785-93e2-47ad-8504-827f22c74aa1.svg)](https://codebeat.co/projects/github-com-stormy102-lancer-develop)|[![Last Develop Commit](https://img.shields.io/github/last-commit/Stormy102/Lancer/develop.svg)](https://github.com/Stormy102/Lancer/commits/develop)|

[![Licence](https://img.shields.io/github/license/Stormy102/Lancer)](#licence)
[![Status](https://img.shields.io/badge/status-Pre%20Release-red.svg)](https://github.com/Stormy102/Lancer/releases)
[![Releases](https://img.shields.io/github/v/release/Stormy102/Lancer?include_prereleases)](https://github.com/Stormy102/Lancer/releases)
![GitHub commits since tagged version (branch)](https://img.shields.io/github/commits-since/Stormy102/Lancer/v0.0.2-alpha/develop)
![GitHub All Releases](https://img.shields.io/github/downloads/Stormy102/Lancer/total)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/Stormy102/Lancer)
[![Contributors](https://img.shields.io/github/contributors/Stormy102/Lancer.svg)](https://github.com/Stormy102/Lancer/graphs/contributors)
![Supported OSs](https://img.shields.io/badge/OS-Windows%20%7C%20Linux%20%7C%20Mac%20OS%20X-blue.svg)
<!--- See for dropping Python 3.5 support https://devguide.python.org/#status-of-python-branches -->
![Python Versions](https://img.shields.io/badge/python-3.5|3.6|3.7|3.8-blue.svg) 
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
![Maintenance](https://img.shields.io/maintenance/yes/2019.svg)
[![Known Vulnerabilities](https://img.shields.io/snyk/vulnerabilities/github/Stormy102/Lancer/requirements.txt.svg)](https://snyk.io/test/github/Stormy102/Lancer?targetFile=requirements.txt)
[![Issues](https://img.shields.io/github/issues/Stormy102/Lancer.svg)](https://github.com/Stormy102/Lancer/issues)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/Stormy102/Lancer)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/Stormy102/Lancer)
![GitHub repo size](https://img.shields.io/github/repo-size/Stormy102/Lancer)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Stormy102/Lancer)

## Introduction

### What is this?

Lancer is a pentesting tool written in [Python 3](https://www.python.org/) which aims to automate and expedite recon and vulnerability scanning.

### *Sigh*... Another pentesting tool? Why should I use this?

The basis of Lancer is to take several tools which already exist, such as [Gobuster](https://github.com/OJ/gobuster/), [Nmap](https://github.com/nmap/nmap), [SMBMap](https://github.com/ShawnDEvans/smbmap) and [many](https://github.com/portcullislabs/enum4linux) [more](https://github.com/sullo/nikto), and intelligently detect which tools should be used depending on the results of a scan, as well as using custom modules to detect other information, such as Geolocation, SSL certificate extraction and more.

This is designed to automate enumeration and analysis of a target/group of targets and make the process of finding vulnerabilities a bit easier.

## Limitations & Upcoming Features

As Lancer is still very much in active development, there is currently limited functionality and it is not recommended for use in a commercial or real-world environment.

<details>
    <summary>Upcoming Features in 0.0.3 (Alpha)</summary> 

* [X] HTTPS support - certificate extraction, normal HTTP services scanning and enumeration _Added in 0.0.3_
* [X] Multiple targets from file support _Added in 0.0.3_
* [X] Convert domain name to IP _Added in 0.0.3_
* [X] IPv4/IPv6 subnet support - `./lancer -T 192.168.0.0/24` _Added in 0.0.3_
* [X] HTTP Service Headers _Added in 0.0.3_
* [X] Get Host Name Module _Added in 0.0.3_
* [X] HTTP method options module _Added in  0.0.3_
* [X] Page Links Module _Added in 0.0.3_
* [X] Output results via JSON to `~/.lancer/cache/[SCAN TIME]/loot.json` _Added in 0.0.3_
* [X] Disable modules from `config.ini` _Added in 0.0.3_
* [X] Output results via terminal console _Added in 0.0.3_
* [X] Write verbose info to log file - outputs info with `-v` and debug with `-vv` _Added for 0.0.3_
* [X] Clear cache command line option - `--clear-cache` _Added in 0.0.3_
* [ ] Improved modularity by shifting to an OOP module approach _Coming in 0.0.3_
    
</details>

<details>
    <summary>Planned Features</summary>

* [ ] Split into blind and targeted modules - blind modules require only a hostname/IP and port, while targeted modules can execute after the blind modules using information potentially harvested from blind modules _Planned for 0.0.4_
* [ ] Modules use hostname and/or IP address correctly _Planned for 0.0.4_
* [ ] MS08-067 vulnerability scan _Planned for 0.0.4_
* [ ] MS17-010 vulnerability scan _Planned for 0.0.4_
* [ ] BlueKeep vulnerability scan _Planned for 0.0.4_
* [ ] RPCClient Null Session module _Planned for 0.0.4_
* [ ] RPCClient User Enumeration _Planned for 0.0.4_
* [ ] Configure intrusiveness level with `-L`/`--level` _Planned for 0.0.4_
* [ ] Change cache root with `--cache-root` _Planned for 0.0.4_
* [ ] Write output to file via `-o` parameter _Planned for 0.0.4_
* [ ] Specify ports to skip scanning _Planned for 0.0.4_
* [ ] Page Links Module use recursion to iterate every available internal link _Planned for 0.0.4_
* [ ] Anonymous LDAP _Planned for 0.0.4_
* [ ] SSLScan for HTTPS _Planned for 0.0.4_
* [ ] SSH support - display fingerprint and SSH version _Planned for 0.0.4_
* [ ] Generate HTML report _Planned for 0.0.4_
* [ ] Limited target attacks. Scans and enumerates specific services only _Planned for 0.0.4_
* [ ] SMB enumeration with SMBClient/smbmap _Planned for 0.0.4_
* [ ] Multi-threading - run all components at the same time, with progress indicator `[!] 3/7 scans complete... /` _Planned for 0.0.4_
* [ ] IPv6 support _Planned for 0.0.4_
* [ ] CPE detection module (making up for removal of old CPE logic) _Coming in 0.0.4_

</details>

<details>
    <summary>Features under evaluation</summary>

* [ ] Localisation support _Planned for 0.0.5_
* [ ] Dig zone transfer _Planned for 0.0.5_
* [ ] WhoIs Module (Maybe use https://api.hackertarget.com/whois/?q={HOST}) _Planned for 0.0.5_
* [ ] Web service screenshots (See [selenium](https://pypi.org/project/selenium/)) _Planned for 0.0.5_
* [ ] Nmap script level _Planned for 0.0.5_
* [ ] enum4linux support _Planned for 0.0.5_
* [ ] Email report _Planned for 0.0.6_
* [ ] WPScan support _Planned for 0.0.6_
* [ ] Open X11 module _Planned for 0.0.6_
* [ ] Metasploit RPC support _Planned for 0.0.7_
* [ ] Extension support - add your own custom report generators and modules _Planned for 0.0.7_
* [ ] Further services detection _Coming soon_
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
* [ ] Further software which may be implemented upon evaluation:
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

</details>

<details>
    <summary>Completed Features</summary>
    
* [X] Nmap scanning _Added in 0.0.1_
* [X] Gobuster enumeration _Added in 0.0.1_
* [X] Searchsploit Nmap results _Added in 0.0.1_
* [X] Configuration file (.ini) for persistent configuration _Added in 0.0.2_
* [X] FTP scanning/downloading files < 50mb _Added in 0.0.2_
* [X] Nikto support _Added in 0.0.2_

</details>

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

Please note that Windows Subsystem for Linux is not officially supported (see [here](https://exploits.run/nmap-wsl/) for techniques to get around the issues present).

To execute the program, ensure that you have Python 3.5 or higher installed. Use Python's pip to install the necessary Python dependencies.
```shell script
pip install -r requirements.txt
```
---
However, Lancer has dependencies on several other external programs being installed. For each of these programs, the environmental PATH variable must point to them so that they can be executed by Python.

|Program|Version|Required|Optional|Linux|Windows|
|---|---|---|---|---|---|
|[Nmap](https://github.com/nmap/nmap)|7.7.0|:heavy_check_mark:| |:heavy_check_mark:|:heavy_check_mark:|
|[Gobuster](https://github.com/OJ/gobuster/releases)|3.1| |:heavy_check_mark:*|:heavy_check_mark:|:heavy_check_mark:|
|[Searchsploit](https://github.com/offensive-security/exploitdb/blob/master/searchsploit)|cbf80e3| |:heavy_check_mark:*|:heavy_check_mark:|:x:|
|[Smbmap](https://github.com/ShawnDEvans/smbmap)|b55fc05| |:heavy_check_mark:*|:heavy_check_mark:|:heavy_check_mark:|
|[Nikto](https://github.com/sullo/nikto)|2.1.6| |:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
|[enum4linux](https://github.com/portcullislabs/enum4linux)|0.8.9| |:heavy_check_mark:|:heavy_check_mark:|:x:|

*_Recommended program_

## Usage

The program takes the following arguments:

```text
usage: lancer.py (-T TARGET | -TF FILE | -TN FILE) [--cache-root PATH]
                 [-L LEVEL] [-a IP] [--skip-ports PORTS [PORTS ...]]
                 [-v | -vv] [-o FILE] [--version] [-l LANGUAGE] [-h]
                 [--clear-cache]

[+] Lancer - system vulnerability scanner
[+] See the config.ini file at C:\Users\Matthew\.lancer\config.ini for more options.

Required Arguments:
  Specify the target or targets that Lancer will scan.

  -T TARGET, --target TARGET
                        The hostname, IPv4 address or a subnet of of IPv4
                        addresses you wish to analyse.
  -TF FILE, --target-file FILE
                        File containing a list of target IP addresses.
  -TN FILE, --target-nmap FILE
                        Skip an internal Nmap scan by providing the path to an
                        Nmap XML file. It is recommended to run common scripts
                        (-sC argument) and version detection (-sV argument)

Module Arguments (Coming soon):
  --cache-root PATH     [NOT YET IMPLEMENTED] The root of the cache. This is
                        where all of the data for the programs run is stored,
                        which may be useful if you wish to document or save
                        all of the data in a separate location.
  -L LEVEL, --level LEVEL
                        [NOT YET IMPLEMENTED] The intrusion level of this
                        iteration. A level of 1 means the least intrusive
                        scripts will be run, such as Nmap on quiet mode and a
                        few HTTP requests. A level of 5 will mean that
                        intrusive exploits will be run against the computer to
                        determine how vulnerable it is. A full list of modules
                        and their intrusion levels can be found on the Github
                        Wiki. This defaults to 3 - moderately intrusive.
  -a IP, --address IP   [NOT YET IMPLEMENTED] Overrides the detected IP
                        address with your own which is supplied.
  --skip-ports PORTS [PORTS ...]
                        [NOT YET IMPLEMENTED] Set the ports to ignore. These
                        ports will have no enumeration taken against them,
                        except for the initial discovery via Nmap. This can be
                        used to run a custom scan and pass the results to
                        Lancer. Best used in conjunction with -TN/--target-
                        nmap.

Output Arguments:
  Control the output of Lancer.

  -v, --verbose         Use a verbose output. This will output results and
                        information as modules run, which can be useful if you
                        don't wish to wait for a report at the end.
  -vv, --very-verbose   Use a very verbose output. This will output virtually
                        every single event that Lancer logs. Useful for
                        debugging.
  -o FILE, --output FILE
                        [NOT YET IMPLEMENTED] Output the human-readable
                        contents of the Lancer scan to a file. Best used in
                        conjunction with -v/-vv
  --version             Shows the current version of Lancer.

Optional Arguments:
  -l LANGUAGE, --language LANGUAGE
                        [NOT YET IMPLEMENTED] Language you want Lancer to use
                        in. The language code uses ISO 639-1. Defaults to
                        English.
  -h, --help            Shows the different arguments available for Lancer.
  --clear-cache         Clear the cache before executing

Examples:
[+] ./lancer -T 10.10.10.100 -v -l de -a 10.8.0.1
[+] ./lancer -TF targets.lan -vv --cache-root ./cache/
[+] ./lancer -TN nmap-10.0.0.1.xml --skip-ports 445 80 -L 5
```

## Contributing

Thanks for your interest in contributing to this project. You can contribute or report issues in the following ways:

### Pull Requests
Before starting a pull request, please communicate to one of the main developers the wishes you would want to make and why. This would best be done in a public forum using [issues](https://github.com/Stormy102/Lancer/issues)

If you would like to create a pull request, please make sure that you are on the [develop branch](https://github.com/Stormy102/Lancer/tree/develop) before opening one. Once you have cloned or forked this repo, open the root of the cloned repo to begin development. This project uses [git-flow](https://github.com/nvie/gitflow) as its branching model.

The current development environment is with [PyCharm](https://www.jetbrains.com/pycharm/)

When making changes, please update the README.md with details of changes to the interface, new environment variables, exposed ports, useful file locations and container parameters.

### Coding Conventions
This project uses [Pep8](https://www.python.org/dev/peps/pep-0008/) to maintain a consistent coding style. PyCharm uses the Pep8 style, which makes conformity easier.  

### Reporting bugs
If you find a bug, crash or any other unintended issue when running the program, please [create an issue](https://github.com/Stormy102/Lancer/issues)

<!-- Contributors how https://github.com/badges/shields/blob/master/README.md has done it? -->

## Credits

See [Credits.md](CREDITS.MD) for the credits

## License

GPL-3.0. See the [LICENSE](LICENCE) file for more details.