from utils import *

import config
import os
import subprocess


def gobuster(url):
    print(normal_message(), "Starting enumeration of", url)
    if config.args.verbose:
        print(normal_message(), "Using wordlist at", config.args.webWordlist)

    if not os.path.exists(config.args.webWordlist):
        print(error_message(), "Wordlist file not found. Skipping enumeration")

    if program_installed("gobuster", True):

        out_file = 'gobuster/gobuster-' + config.args.target + '.txt.'

        if config.args.verbose:
            print(normal_message(), "Writing gobuster data to", out_file)

        print(normal_message(), "Enumerating directories on", url + "...")

        output = subprocess.check_output(['gobuster', 'dir', '-w', config.args.webWordlist, '-u', url,
                                              '-o', out_file]).decode('UTF-8')

        # Clear Gobuster's Progress: X / Y (ZZ.ZZ%)
        sys.stdout.write('\x1b[2K')

        if config.args.show_output:
            print("")
            print(output)

        parse_gobuster_results(out_file)


def parse_gobuster_results(gobuster_file):
    # Open the file
    with open(gobuster_file, 'r') as file:
        # Loop through every line in the file
        for response_line in file:
            # Get the response code (last three chars but two
            # import sys)
            code = response_line[-5:-2]
            # Get this as a human readable response
            human_readable_code = get_http_code(int(code))
            # Get the directory
            response_dir = response_line.split('(')[0].strip()
            print(warning_message(), "Directory found at", response_dir, "with response", human_readable_code,
                  "(" + code + ")")


def nikto(url):
    print(normal_message(), "Starting scan of", url)

    if program_installed("nikto", False):
        print(error_message(), "Nikto is not yet supported")
