from modules.legacy.web import nikto


def test_nikto():
    url = "http://scanme.nmap.org"
    nikto.exec(url)