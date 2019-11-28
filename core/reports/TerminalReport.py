# -*- coding: utf-8 -*-
"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.reports.Report import Report
from shutil import get_terminal_size

import textwrap
import pyfiglet


class TerminalReport(Report):

    def __init__(self):
        super(TerminalReport, self).__init__()

    def generate_report(self, data: dict) -> None:
        self.print_line()

        text = pyfiglet.figlet_format("Scan Report", "standard")
        term_size = get_terminal_size((80, 24))

        header = '\n'.join(x.center(term_size.columns) for x in text.splitlines())
        print(header)

        self.print_line()

        for target in data:
            print(" Target: {HOST}".format(HOST=target))
            for port in data[target]:
                if self.is_port(port):
                    print(" " * 3 + "Port: {HOST}".format(HOST=port))
                else:
                    print(" " * 3 + "{HOST}".format(HOST=port))
                self.generate_info_from_data(data[target][port], 6)
            self.print_line()

    # noinspection PyMethodMayBeStatic
    def generate_info_from_data(self, data: dict, depth: int) -> None:
        for item in data:
            if isinstance(data[item], dict):
                print(" " * depth + "{ITEM}:".format(ITEM=item))
                if data[item]:
                    self.generate_info_from_data(data[item], depth+3)
                else:
                    print(" " * (depth + 3) + "No results")
            elif isinstance(data[item], list):
                print(" " * depth + "{ITEM}:".format(ITEM=item))
                if data[item]:
                    for entry in data[item]:
                        print(" " * (depth + 3) + "- {ENTRY}".format(ENTRY=entry))
                else:
                    print(" " * (depth + 3) + "No results")
            else:
                if isinstance(data[item], str):
                    if data[item]:
                        lines = data[item].splitlines()
                        print(" " * depth + "{ITEM}: {VALUE}".format(ITEM=item, VALUE=lines[0]))
                        # If there is more than one line, display them neatly line by line
                        for x in range(1, len(lines)):
                            print(" " * (depth + 2 + len(item)) + lines[x])
                    else:
                        print(" " * depth + "No results")
                else:
                    print(" " * depth + "{ITEM}: {VALUE}".format(ITEM=item, VALUE=data[item]))

    # noinspection PyMethodMayBeStatic
    def print_line(self):
        width = get_terminal_size((80, 24)).columns
        print()
        print("=" * width)
        print()

    # noinspection PyMethodMayBeStatic
    def is_port(self, s) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False
