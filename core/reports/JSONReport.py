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
        super(JSONReport, self).__init__()
        self.filename = "output.json"

    def generate_report(self, data: dict) -> None:
        with open(os.path.join(config.get_report_folder(), self.filename), "w") as file:
            json_data = json.dumps(data, sort_keys=False, indent=4)
            file.write(json_data)
