# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.GenericWebServiceModule import GenericWebServiceModule
from core import config

import os
import imgkit


class GetWebsiteScreenshot(GenericWebServiceModule):

    def __init__(self):
        super(GetWebsiteScreenshot, self).__init__(name="Get Website Screenshot",
                                                   description="Screenshots any websites",
                                                   loot_name="web-screenshots",
                                                   intrusion_level=2)

    def execute(self, ip: str, port: int) -> None:
        """
        Take a screenshot of the website
        :param ip: IP to use
        :param port: Port to use
        :return:
        """
        # TODO: Wkhtmltoimage seems veeeeeery slow - maybe evaluate Selenium before release

        url = self.get_url(ip, port)

        path = os.path.join(config.get_module_cache(self.name, ip, str(port)), "screenshot.png")
        self.logger.debug("Taking screenshot")
        try:
            imgkit.from_url(url, path)
            self.logger.info("Screenshot saved to {PATH}".format(PATH=path))
        except OSError:
            self.logger.error("Unable to connect to {URL}".format(URL=url))
