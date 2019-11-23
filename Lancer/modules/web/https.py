import ssl
import utils
import OpenSSL
import ssl


def exec(url, port):
    get_https_cert_values(url, port)


def get_https_cert_values(url, port):
    try:
        cert = ssl.get_server_certificate((url, port), ssl_version=ssl.PROTOCOL_SSLv23)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        cert_details = x509.get_subject().get_components()
        print(utils.normal_message(), "Retrieved certificate from", url + ":" + str(port))
        for entry in cert_details:
            if entry[0].decode("utf-8") == 'CN':
                print(utils.warning_message(), "Common name is", entry[1].decode("utf-8"))
    except ssl.SSLError:
        # See here for why it fails on Cloudflare etc.
        # https://stackoverflow.com/questions/53683537/python-error-ssl-ssl-sslerror-ssl-sslv3-alert-handshake-failure-sslv3-alert
        print(utils.error_message(), "Unable to retrieve common name. This often occurs due to several domains\n    "
                                     "which could resolve to one IP address, such as through a network like\n    "
                                     "Cloudflare")
    print()