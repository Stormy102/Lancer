import ssl
import utils
# import M2Crypto


def get_https_cert_values(url, port):
    cert = ssl.get_server_certificate((url, port))
    # x509 = M2Crypto.X509.load_cert_string(cert)
    # x509.get_subject().as_text()
    print(utils.normal_message(), "Retrieved certificate from", url + ":" + port)
