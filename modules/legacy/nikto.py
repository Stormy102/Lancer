from xml.dom import minidom

import subprocess
from core import config, utils
import os


def exec(url):
    print(utils.normal_message(), "Starting scan of", url, "with Nikto")

    if utils.program_installed("Nikto", False):

        out_file = os.path.join(config.nikto_cache(), 'nikto-' + url + '.xml')
        # Replace the colon for sanitised filename
        out_file = out_file.replace('http://', '')
        out_file = out_file.replace('https://', '')
        out_file = out_file.replace(':', '-')

        output = subprocess.check_output(['nikto', '-host', url, "-Format", "xml", "-o", out_file, "-ask", "no"])\
            .decode('UTF-8')

        # if config.args.show_output:
        #    print()
        #    print(output)

        parse_nikto_xml(out_file)
        print()


def parse_nikto_xml(out_file):
    xmldoc = minidom.parse(out_file)
    nikto_items = xmldoc.getElementsByTagName('item')

    for item in nikto_items:
        print(utils.warning_message(), item.getElementsByTagName("description")[0].firstChild.wholeText)
