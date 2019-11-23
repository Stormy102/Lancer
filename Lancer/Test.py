from modules.new.SSLCertificateExtractor import SSLCertificateExtractor
import Loot

cert = SSLCertificateExtractor()
print(cert.can_execute_module())
cert.execute("207.180.207.193", 443)
cert.execute("google.co.uk", 443)
cert.execute("self-signed.badssl.com", 443)
cert.execute("expired.badssl.com", 443)
cert.execute("c2.mdawson.dev", 443)

Loot.to_json()
