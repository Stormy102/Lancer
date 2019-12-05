# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.BaseModule import BaseModule


class Searchsploit(BaseModule):

    def __init__(self):
        super(Searchsploit, self).__init__(name="Searchsploit",
                                           description="Looks up detected services on exploit-db",
                                           loot_name="exploit-db",
                                           multithreaded=False,
                                           intrusive=False,
                                           critical=False)
        self.required_programs = ["searchsploit"]
