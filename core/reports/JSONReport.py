# -*- coding: utf-8 -*-
"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.reports.Report import Report
from core import config

import json
import os


class JSONReport(Report):

    def __init__(self):
        super(JSONReport, self).__init__("JSON Report")
        self.filename = "output.json"

    def generate_report(self, data: dict) -> None:
        """
        Generate a JSON file with the loot data in
        :param data:
        """
        path = os.path.join(config.get_report_folder(), self.filename)
        with open(path, "w") as file:
            json_data = json.dumps(data, sort_keys=False, indent=4)
            file.write(json_data)
            self.logger.info("Wrote report to {PATH}".format(PATH=path))
