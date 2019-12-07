"""from core import ArgHandler, config
import os
import urllib.request


def gobuster():

    urllib.request.urlretrieve(
        'https://raw.githubusercontent.com/thesp0nge/enchant/master/db/directory-list-2.3-medium.txt',
        'directory-list-2.3-medium.txt')

    assert os.path.exists('directory-list-2.3-medium.txt')

    config.config['Web']['DefaultWordlist'] = 'directory-list-2.3-medium.txt'
    ArgHandler.parse_arguments(['-T', '127.0.0.1'])

    url = "http://scanme.nmap.org"
    # http.gobuster(url)
"""
