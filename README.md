# Lancer v0.1.0 Alpha

<p align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#limitations--upcoming-features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a>
</p>

<p align="center">
    <a href="LICENCE" alt="Licence">
        <img src="https://img.shields.io/github/license/Stormy102/Lancer?style=flat-square" /></a>
    <a href="#backers" alt="Releases">
        <img src="https://img.shields.io/github/v/release/Stormy102/Lancer?include_prereleases&style=flat-square&color=blue" /></a>
    <a href="https://github.com/Stormy102/Lancer/issues" alt="Issues">
        <img src="https://img.shields.io/github/issues/Stormy102/Lancer?style=flat-square" /></a>
    <a href="https://github.com/Stormy102/Lancer/releases" alt="Downloads">
        <img src="https://img.shields.io/github/downloads/Stormy102/Lancer/total?style=flat-square" /></a>
    <a href="https://github.com/Stormy102/Lancer/pulse" alt="Maintenance">
        <img src="https://img.shields.io/maintenance/yes/2019?style=flat-square" /></a>
    <a href="https://snyk.io/test/github/Stormy102/Lancer?targetFile=requirements.txt" alt="Vulnerabilities">
        <img src="https://img.shields.io/snyk/vulnerabilities/github/Stormy102/Lancer/requirements.txt?style=flat-square" alt="Vulnerabilities"></a>
    <a href="#installation" alt="Supported OSs">
        <img src="https://img.shields.io/badge/Supported%20OSs-Windows%207+%20%7C%20Ubuntu/Debian-purple.svg?style=flat-square"
            alt="Support OSs"></a>
    <a href="#installation">
        <!--- See for dropping Python 3.5 support https://devguide.python.org/#status-of-python-branches -->
        <img src="https://img.shields.io/badge/python-3.5+-yellow.svg?style=flat-square"
            alt="coverage"></a>
    <a href="https://www.python.org/dev/peps/pep-0008/" alt="Pep8 style">
        <img src="https://img.shields.io/badge/code%20style-pep8-darkred?style=flat-square"
            alt="Total alerts"/></a>
    <a>
        <img src="https://img.shields.io/github/languages/code-size/Stormy102/Lancer?style=flat-square"
            alt="commits to be deployed"></a>
</p>

|Branch | Status                                                                                                                                                 | Coverage                                                                                                                                                            | Code Quality                                                                                                                                                   | Last Commit                                                                                                                                                       |Commits since last release                                                                                                                                                                                             |
|-------|--------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Master |[![Build Status](https://img.shields.io/travis/com/Stormy102/Lancer?style=flat-square)](https://travis-ci.com/Stormy102/Lancer/branches)                |[![Coverage Status](https://img.shields.io/coveralls/github/Stormy102/Lancer?style=flat-square)](https://coveralls.io/github/Stormy102/Lancer)                       |[![Master Code Quality](https://codebeat.co/badges/08113589-61c1-418c-8f2e-bffcc5562425)](https://codebeat.co/projects/github-com-stormy102-lancer-master)      |[![Last Master Commit](https://img.shields.io/github/last-commit/Stormy102/Lancer?style=flat-square)](https://github.com/Stormy102/Lancer/commits/master)          |![Commits since release](https://img.shields.io/github/commits-since/Stormy102/Lancer/master?label=Commits%20since%20last%20release&style=flat-square)                                                                 |
|Develop|[![Develop Build Status](https://img.shields.io/travis/com/Stormy102/Lancer/develop?style=flat-square)](https://travis-ci.com/Stormy102/Lancer/branches)|[![Coverage Status](https://img.shields.io/coveralls/github/Stormy102/Lancer/develop?style=flat-square)](https://coveralls.io/github/Stormy102/Lancer?branch=develop)|[![Develop Code Quality](https://codebeat.co/badges/10ed4785-93e2-47ad-8504-827f22c74aa1.svg)](https://codebeat.co/projects/github-com-stormy102-lancer-develop)|[![Last Develop Commit](https://img.shields.io/github/last-commit/Stormy102/Lancer/develop?style=flat-square)](https://github.com/Stormy102/Lancer/commits/develop)|[![Commits since release](https://img.shields.io/github/commits-since/Stormy102/Lancer/develop?label=Commits%20since%20last%20release&style=flat-square)](https://github.com/Stormy102/Lancer/compare/master...develop)|

As the project uses the [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model, work is not just shown on the Master and Develop branches - there are [other branches](https://github.com/Stormy102/Lancer/branches) for this project.  

<sub><i>Some modules involve software which cannot be tested on public CI servers. These tests can often by run from the local computer with `pytest --run-no-ci`. Look in [.coveragerc](.coveragerc) for more info regarding code not included in coverage.</i></sub>

## Introduction

### What is this?

Lancer is a pentesting tool written in [Python 3](https://www.python.org/) which aims to automate and expedite recon and vulnerability scanning.

### *Sigh*... Another pentesting tool? Why should I use this?

The basis of Lancer is to take several tools which already exist, such as [Gobuster](https://github.com/OJ/gobuster/), [Nmap](https://github.com/nmap/nmap), [smbclient](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html) and [many](https://github.com/portcullislabs/enum4linux) [more](https://github.com/sullo/nikto), and intelligently detect which tools should be used depending on the results of a scan, as well as using custom modules to detect other information, such as Geolocation, SSL certificate extraction and more.

This is designed to automate enumeration and analysis of a target/group of targets and make the process of finding vulnerabilities a bit easier.

## Limitations & Upcoming Features

As Lancer is still very much in active development, there is currently limited functionality and it is not recommended for use in a commercial or real-world environment.

<details>
    <summary>Completed Features</summary>

* [X] HTTPS support - certificate extraction, normal HTTP services scanning and enumeration _Added in 0.1.0_
* [X] Multiple targets from file support _Added in 0.1.0_
* [X] Convert domain name to IP _Added in 0.1.0_
* [X] IPv4/IPv6 subnet support - `./lancer -T 192.168.0.0/24` _Added in 0.1.0_
* [X] HTTP Service Headers _Added in 0.1.0_
* [X] Get Host Name Module _Added in 0.1.0_
* [X] HTTP method options module _Added in 0.1.0_
* [X] Page Links Module _Added in 0.1.0_
* [X] Output results via JSON to `~/.lancer/cache/[SCAN TIME]/loot.json` _Added in 0.1.0_
* [X] Disable modules from `config.ini` _Added in 0.1.0_
* [X] Output results via terminal console _Added in 0.1.0_
* [X] Write verbose info to log file - outputs info with `-v` and debug with `-vv` _Added for 0.1.0_
* [X] Clear cache command line option - `--clear-cache` _Added in 0.1.0_
* [X] Improved modularity by shifting to an OOP module approach _Added in 0.1.0_
* [X] Specify ports to skip scanning _Added in 0.1.0_
* [X] Event-driven system instead of single port scan loop _Added in 0.1.0_
* [X] Configuration file (.ini) for persistent configuration _Added in 0.0.2_
* [X] FTP scanning/downloading files < 50mb _Added in 0.0.2_
* [X] Nikto support _Added in 0.0.2_
* [X] Nmap scanning _Added in 0.0.1_
* [X] Gobuster enumeration _Added in 0.0.1_
* [X] Searchsploit Nmap results _Added in 0.0.1_

</details>

<details>
    <summary>Upcoming Features in 0.2.0 (Alpha)</summary> 

* [ ] Multi-threading - run all components at the same time, with progress indicator `[!] 3/7 scans complete... /` _Planned for 0.2.0_
* [ ] Split into blind and targeted modules - blind modules require only a hostname/IP and port, while targeted modules can execute after the blind modules using information potentially harvested from blind modules _Planned for 0.2.0_
* [X] Configure intrusiveness level with `-L`/`--level` _Planned for 0.2.0_
* [ ] Change cache root with `--cache-root` _Planned for 0.2.0_
* [ ] IPv6 support _Planned for 0.2.0_
* [ ] Page Links Module use recursion to iterate every available internal link _Planned for 0.2.0_
* [ ] Generate HTML report _Planned for 0.2.0_
* [ ] Auto-updater from Github _Planned for 0.2.0_
* [ ] Specify custom warning cache size _Planned for 0.2.0_
* [ ] HTTP Options brute forcing _Planned for 0.2.0_
* [ ] Specify custom download size for FTP Anonymous Download _Planned for 0.2.0_
* [ ] Modules use hostname and/or IP address correctly _Planned for 0.2.0_
* [ ] Quiet Nmap scan using -sS _Planned for 0.2.0_
* [ ] Option for Nmap UDP _Planned for 0.2.0_
* [ ] Option for full Nmap port scan _Planned for 0.2.0_
* [X] SSH support - display banner, fingerprint and SSH version _Planned for 0.2.0_
* [X] Telnet banner support _Planned for 0.2.0_
* [X] MS08-067 vulnerability scan _Planned for 0.2.0_
* [X] MS17-010 vulnerability scan _Planned for 0.2.0_
* [ ] BlueKeep vulnerability scan _Planned for 0.2.0_
* [ ] [SSL version detection/vulnerabilities](https://pypi.org/project/sslscan/) _Planned for 0.2.0_
* [X] SMB Null Session module _Planned for 0.2.0_
* [X] SMB Shares module _Planned for 0.2.0_
* [ ] SMB Get OS Version _Planned for 0.2.0_
* [ ] CPE detection module (making up for removal of old CPE logic) _Coming in 0.2.0_
* [ ] RPCClient Null Session module _Planned for 0.2.0_
* [ ] RPCClient User Enumeration _Planned for 0.2.0_

</details>

<details>
    <summary>Planned features</summary>

* [ ] Greater extension support/documentation - add your own custom report generators and modules _Planned for 0.3.0_
* [ ] Localisation support _Planned for 0.3.0_
* [ ] Write output to file via `-o` parameter _Planned for 0.3.0_
* [ ] Anonymous LDAP _Planned for 0.3.0_
* [ ] Dig zone transfer _Planned for 0.3.0_
* [ ] WhoIs Module (Maybe use https://api.hackertarget.com/whois/?q={HOST}) _Planned for 0.3.0_
* [ ] Web service screenshots (See [selenium](https://pypi.org/project/selenium/)) _Planned for 0.3.0_
* [ ] Nmap script level _Planned for 0.3.0_
* [ ] Limited target attacks. Scans and enumerates specific services only _Planned for 0.3.0_
* [ ] enum4linux support _Planned for 0.3.0_
* [ ] Email report _Planned for 0.4.0_
* [ ] WPScan support _Planned for 0.4.0_
* [ ] Open X11 module _Planned for 0.4.0_
* [ ] Metasploit RPC support _Planned for 0.5.0_
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

Any other features you want to see? Open a Github Issue or a pull request.

## Installation

To get started with Lancer, either run `git clone https://github.com/Stormy102/Lancer` to clone the repository or download the zip from Github with Clone or Download > Download Zip

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

| Program                                                                                |Version|Required          | Optional          | Linux            | Windows          |
|----------------------------------------------------------------------------------------|-------|------------------|-------------------|------------------|------------------|
|[Nmap](https://github.com/nmap/nmap)                                                    |7.7.0  |:heavy_check_mark:|                   |:heavy_check_mark:|:heavy_check_mark:|
|[Gobuster](https://github.com/OJ/gobuster/releases)                                     |3.1    |                  |:heavy_check_mark:*|:heavy_check_mark:|:heavy_check_mark:|
|[Searchsploit](https://github.com/offensive-security/exploitdb/blob/master/searchsploit)|cbf80e3|                  |:heavy_check_mark:*|:heavy_check_mark:|:x:               |
|[Nikto](https://github.com/sullo/nikto)                                                 |2.1.6  |                  |:heavy_check_mark: |:heavy_check_mark:|:heavy_check_mark:|

*_Recommended program_

## Usage

The program takes the following arguments:

```text
usage: lancer.py (-T TARGET | -TF FILE | -TN FILE) [-L LEVEL]
                 [--skip-ports PORTS [PORTS ...]] [-v | -vv] [--version]
                 [-l LANGUAGE] [-h] [--clear-cache]

[+] Lancer - system vulnerability scanner
[+] See the config.ini file at ~/.lancer/config.ini for more options.

Required Arguments:
  Specify the target or targets that Lancer will scan.

  -T TARGET, --target TARGET
                        The hostname, IPv4 address or a subnet of of IPv4
                        addresses you wish to analyse.
  -TF FILE, --target-file FILE
                        File containing a list of target IP addresses.
  -TN FILE, --target-nmap FILE
                        Skip an internal Nmap scan by providing the path to an
                        Nmap XML file. It is recommended to run version
                        detection (-sV argument)

Module Arguments:
  -L LEVEL, --level LEVEL
                        The intrusion level of this iteration. A level of 1
                        means the least intrusive scripts will be run, such as
                        Nmap on quiet mode and a few HTTP requests. A level of
                        5 will mean that intrusive exploits will be run
                        against the computer to determine how vulnerable it
                        is. A full list of modules and their intrusion levels
                        can be found on the Github Wiki. This defaults to 3 -
                        moderately intrusive.
  --skip-ports PORTS [PORTS ...]
                        Set the ports to ignore. These ports will have no
                        enumeration taken against them, except for the initial
                        discovery via Nmap. This can be used to run a custom
                        scan and pass the results to Lancer. Best used in
                        conjunction with -TN/--target-nmap.

Output Arguments:
  Control the output of Lancer.

  -v, --verbose         Use a verbose output. This will output results and
                        information as modules run, which can be useful if you
                        don't wish to wait for a report at the end.
  -vv, --very-verbose   Use a very verbose output. This will output virtually
                        every single event that Lancer logs. Useful for
                        debugging.
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
Before starting a pull request, please communicate to one of the main developers the changes you would want to make and why. This would best be done in a public forum using [issues](https://github.com/Stormy102/Lancer/issues)

If you would like to create a pull request, please make sure that you are on the [develop branch](https://github.com/Stormy102/Lancer/tree/develop) before opening one. Once you have cloned or forked this repo, open the root of the cloned repo to begin development. This project uses [git-flow](https://github.com/nvie/gitflow) as its branching model.

The current development environment is with [PyCharm](https://www.jetbrains.com/pycharm/)

When making changes, please update the README.md with details of changes to the command line interface, command line arguments, new environment variables, new file locations and container parameters.

### Coding Conventions
This project uses [Pep8](https://www.python.org/dev/peps/pep-0008/) to maintain a consistent coding style. PyCharm uses the Pep8 style, which makes conformity easier.  

### Reporting bugs
If you find a bug, crash or any other unintended issue when running the program, please [create an issue](https://github.com/Stormy102/Lancer/issues/new). If you believe the issue is a security flaw, please consult [our security policy](.github/SECURITY.md).

<!-- Contributors how https://github.com/badges/shields/blob/master/README.md has done it? -->

## Credits

See [Credits.md](.github/CREDITS.MD) for the credits

## License

GPL-3.0. See the [LICENSE](LICENCE) file for more details.