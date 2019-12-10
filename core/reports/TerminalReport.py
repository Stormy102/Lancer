# -*- coding: utf-8 -*-
"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.reports.Report import Report
from shutil import get_terminal_size

import pyfiglet


class TerminalReport(Report):

    def __init__(self):
        super(TerminalReport, self).__init__("Terminal Report")

    def generate_report(self, data: dict) -> None:
        """
        Generate a terminal report
        :param data: Data to format
        """

        self.print_line()

        # Header figlet
        text = pyfiglet.figlet_format("Scan Report", "standard")
        term_size = get_terminal_size((80, 24))

        header = '\n'.join(x.center(term_size.columns) for x in text.splitlines())
        print(header)

        self.print_line()

        # Loop through each target
        for target in data:
            print(" Target: {HOST}".format(HOST=target))
            for port in data[target]:
                # Loop through each sub item. If it's a port:
                if self.is_port(port):
                    print(" " * 3 + "Port: {HOST}".format(HOST=port))
                # If its module results it won't be a number
                else:
                    print(" " * 3 + "{HOST}".format(HOST=port))
                self.generate_info_from_data(data[target][port], 6)
            self.print_line()
        self.logger.debug("Finished generating Terminal report")

    # noinspection PyMethodMayBeStatic
    def generate_info_from_data(self, data: dict, depth: int) -> None:
        # Loop through the data in the dictionary
        for item in data:
            # If it's a dictionary
            if isinstance(data[item], dict):
                self.handle_dict_output(item, data, depth)
            # If it's a list
            elif isinstance(data[item], list):
                self.handle_list_output(item, data, depth)
            else:
                # If it's a string
                if isinstance(data[item], str):
                    self.handle_str_output(item, data[item], depth)
                # Any other data time, just print as str
                else:
                    print(" " * depth + "{ITEM}: {VALUE}".format(ITEM=item, VALUE=data[item]))

    def handle_dict_output(self, item: str, data: dict, depth: int) -> None:
        """
        Parse a dictionary to display on the Terminal Report
        :param item: The current key of the dictionary
        :param data: The dictionary
        :param depth: The current depth of the report
        """
        # Create a heading
        print(" " * depth + "{ITEM}:".format(ITEM=item))
        # If it's got data, recursively call
        if data[item]:
            self.generate_info_from_data(data[item], depth + 3)
        # No data
        else:
            print(" " * (depth + 3) + "No results")

    # noinspection PyMethodMayBeStatic
    def handle_list_output(self, item: str, data: dict, depth: int) -> None:
        """
        Parse a list to display on the Terminal Report
        :param item: The key from the dictionary
        :param data: The dictionary of data
        :param depth: The current depth of the report
        """
        print(" " * depth + "{ITEM}:".format(ITEM=item))
        # If the list has items
        if data[item]:
            for entry in data[item]:
                # If it's a dictionary, then
                if isinstance(entry, dict):
                    # Iterate through the dictionary if valid
                    if entry:
                        # Print every line
                        for value in entry:
                            print(" " * (depth + 3) + "{ITEM}: {VALUE}".format(ITEM=value, VALUE=entry[value]))
                    else:
                        print(" " * (depth + 3) + "No results")
                else:
                    print(" " * (depth + 3) + "- {ENTRY}".format(ENTRY=entry))
        else:
            print(" " * (depth + 3) + "No results")

    # noinspection PyMethodMayBeStatic
    def handle_str_output(self, item: str, data: str, depth: int) -> None:
        """
        Parse a string to display on the Terminal Report
        :param item: The item (key) from the dictionary
        :param data: The string data
        :param depth: The current depth of the report
        """
        # If the data item is valid
        if data:
            # Split into lines
            lines = data.splitlines()
            # Print the first item
            print(" " * depth + "{ITEM}: {VALUE}".format(ITEM=item, VALUE=lines[0]))
            # If there is more than one line, display them neatly line by line
            for x in range(1, len(lines)):
                print(" " * (depth + 2 + len(item)) + lines[x])
        else:
            print(" " * depth + "{ITEM}: No results".format(ITEM=item))

    # noinspection PyMethodMayBeStatic
    def print_line(self) -> None:
        """
        Print a line of ==
        """
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
