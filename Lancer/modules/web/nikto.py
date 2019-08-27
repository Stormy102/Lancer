import utils
import subprocess
import config
import os


def nikto(url):
    print(utils.normal_message(), "Starting scan of", url)

    if utils.program_installed("Nikto", False):

        out_file = os.path.join(config.nikto_cache(), 'nikto-' + url + '.txt.')
        # Replace the colon for sanitised filename
        out_file = out_file.replace('http://', '')
        out_file = out_file.replace('https://', '')
        out_file = out_file.replace(':', '-')

        output = subprocess.check_output(['nikto', '-Host', url, "-Format", "txt", "-o", out_file]).decode('UTF-8')

        if config.args.show_output:
            print("")
            print(output)

        print(utils.warning_message(), "Nikto output parsing coming soon...")
        print("")
