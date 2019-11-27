from core import Loot, ModuleProvider  # , localisation
from modules.FTPAnonymousAccess import FTPAnonymousAccess
from modules.FTPBanner import FTPBanner
from modules.GeolocateIP import GeolocateIP
from modules.Gobuster import Gobuster
from modules.HTTPHeaders import HTTPHeaders
from modules.Nikto import Nikto
from modules.SSLCertificateExtractor import SSLCertificateExtractor
from modules.GetHostname import GetHostname
from modules.Nmap import Nmap
from modules.HTTPOptions import HTTPOptions
from modules.GetWebsiteLinks import GetWebsiteLinks

nmap = Nmap()

ftpanon = FTPAnonymousAccess()
ftpanon.execute("speedtest.tele2.net", 21)

ftpbanner = FTPBanner()
ftpbanner.execute("speedtest.tele2.net", 21)

geo_ip = GeolocateIP()
geo_ip.execute("speedtest.tele2.net", 80)
geo_ip.execute("self-signed.badssl.com", 80)
geo_ip.execute("expired.badssl.com", 80)
geo_ip.execute("c2.mdawson.dev", 80)

cert = SSLCertificateExtractor()
cert.execute("c2.mdawson.dev", 443)
cert.execute("self-signed.badssl.com", 443)
cert.execute("expired.badssl.com", 443)

gobuster = Gobuster()
# gobuster.execute("localhost", 80)
# gobuster.execute('expired.badssl.com', 443)
# gobuster.execute("self-signed.badssl.com", 443)
# gobuster.execute('speedtest.tele2.net', 80)

nikto = Nikto()
nikto.execute("c2.mdawson.dev", 80)
nikto.execute('expired.badssl.com', 443)
nikto.execute("self-signed.badssl.com", 443)
nikto.execute('speedtest.tele2.net', 80)

headers = HTTPHeaders()
headers.execute("mdawson.dev", 443)

hostname = GetHostname()
hostname.execute("127.0.0.1", 0)

options = HTTPOptions()
options.execute("apache.org", 80)
options.execute("www.mdawson.dev", 443)

links = GetWebsiteLinks()
links.execute("mdawson.dev", 80)

# print(Loot.to_json())

# ModuleProvider.main()

ModuleProvider.check_module_dependencies()
