import ssl
import utils
import OpenSSL


def get_https_cert_values(url, port):
    cert = ssl.get_server_certificate((url, port), ssl_version=ssl.PROTOCOL_SSLv23)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    cert_details = x509.get_subject().get_components()
    print(utils.normal_message(), "Retrieved certificate from", url + ":" + str(port))
    for entry in cert_details:
        if entry[0].decode("utf-8") == 'CN':
            print(utils.warning_message(), "Common name is", entry[1].decode("utf-8"))
