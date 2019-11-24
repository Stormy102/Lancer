from core import config, utils
import os
import subprocess
import sys


def exec(url):
    print(utils.normal_message(), "Starting enumeration of", url, "with Gobuster")

    wordlist_path = get_wordlist_path()
    if config.args.verbose:
        print(utils.normal_message(), "Using wordlist at", wordlist_path)

    if os.path.exists(wordlist_path) is False:
        print(utils.error_message(), "Wordlist file not found. Skipping enumeration...")
    elif utils.program_installed("Gobuster", True):
        out_file = os.path.join(config.gobuster_cache(), 'gobuster-' + url + '.txt.')
        # Replace the colon for sanitised filename
        out_file = out_file.replace('http://', '')
        out_file = out_file.replace('https://', '')
        out_file = out_file.replace(':', '-')

        if config.args.verbose:
            print(utils.normal_message(), "Writing gobuster data to", out_file)

        print(utils.normal_message(), "Enumerating directories on", url + "...")

        output = subprocess.check_output(['gobuster', 'dir', '-w', wordlist_path, '-u', url, '-o', out_file])\
            .decode('UTF-8')
        # Clear Gobuster's Progress: X / Y (ZZ.ZZ%)
        sys.stdout.write('\x1b[2K')

        if config.args.show_output:
            print("")
            print(output)

        parse_gobuster_results(out_file)
    print()


def get_wordlist_path():
    if config.args.webWordlist != '':
        return config.args.webWordlist
    return config.config['Web']['DefaultWordlist']


def parse_gobuster_results(gobuster_file):
    # Open the file
    with open(gobuster_file, 'r') as file:
        # Loop through every line in the file
        responses = []
        for response_line in file:
            # Get the response code (last three chars but two
            # import sys)
            code = response_line[-5:-2]
            # Get this as a human readable response
            human_readable_code = utils.get_http_code(int(code))
            # Get the directory
            response_dir = response_line.split('(')[0].strip()
            responses.append("Directory found at " + response_dir + " with response " + human_readable_code +
                             " (" + code + ")")

        response_count = len(responses)
        if response_count > 0:
            print(utils.warning_message(), response_count, "found")
            for response in responses:
                print(utils.warning_message(), response)
        else:
            print(utils.error_message(), "No directories found")
