# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.BaseModule import BaseModule
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization

import datetime
from core import Loot
import OpenSSL
import idna
import socket


class SSLCertificateExtractor(BaseModule):
    def __init__(self):
        super(SSLCertificateExtractor, self).__init__(name="SSL Certificate Extractor",
                                                      description="Extracts an SSL certificate from a HTTP server",
                                                      loot_name="SSL Cert Extract",
                                                      multithreaded=False,
                                                      intrusive=False,
                                                      critical=False)

    def execute(self, ip: str, port: int) -> None:
        # A lot of the work getting this to work with SNI
        # certificates came from gdamjan. Many thanks!
        # https://gist.github.com/gdamjan/55a8b9eec6cf7b771f92021d93b87b2c

        hostname_idna = idna.encode(ip)
        sock = socket.socket()

        sock.connect((ip, port))
        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)  # most compatible
        ctx.check_hostname = False
        ctx.verify_mode = OpenSSL.SSL.VERIFY_NONE

        sock_ssl = OpenSSL.SSL.Connection(ctx, sock)
        sock_ssl.set_connect_state()
        sock_ssl.set_tlsext_host_name(hostname_idna)
        try:
            sock_ssl.do_handshake()
        except OpenSSL.SSL.Error:
            # TODO: Don't quietly return
            return
        cert = sock_ssl.get_peer_certificate()
        crypto_cert = cert.to_cryptography()
        sock_ssl.close()
        sock.close()

        # Now we've got the SSL cert, create the SSL certificate components
        self.create_loot_space(ip=ip, port=port)

        data = Loot.loot[ip][str(port)][self.loot_name]

        try:
            names = crypto_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
            common_name = names[0].value
        except x509.ExtensionNotFound:
            common_name = None
        except IndexError:
            common_name = None
        data["Common Name"] = common_name

        try:
            ext = crypto_cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
            alt_names = ext.value.get_values_for_type(x509.DNSName)
        except x509.ExtensionNotFound:
            alt_names = None
        data["Alt Names"] = alt_names

        data["Issue Date"] = str(crypto_cert.not_valid_before)
        data["Expiry Date"] = str(crypto_cert.not_valid_after)

        expired = crypto_cert.not_valid_after < datetime.datetime.now()

        data["Expired"] = expired

        try:
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.COUNTRY_NAME)
            country_name = names[0].value
        except x509.ExtensionNotFound:
            country_name = None
        data["Country"] = country_name

        try:
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)
            province_name = names[0].value
        except x509.ExtensionNotFound:
            province_name = None
        except IndexError:
            province_name = None
        data["Province"] = province_name

        try:
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.LOCALITY_NAME)
            locality_name = names[0].value
        except x509.ExtensionNotFound:
            locality_name = None
        except IndexError:
            locality_name = None
        data["Locality"] = locality_name

        try:
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)
            organization_name = names[0].value
        except x509.ExtensionNotFound:
            organization_name = None
        data["Organisation Name"] = organization_name

        try:
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)
            organizational_unit_name = names[0].value
        except x509.ExtensionNotFound:
            organizational_unit_name = None
        except IndexError:
            organizational_unit_name = None
        data["OU"] = organizational_unit_name

        try:
            emails = crypto_cert.issuer.get_attributes_for_oid(NameOID.EMAIL_ADDRESS)
            email_address = emails[0].value
        except x509.ExtensionNotFound:
            email_address = None
        except IndexError:
            email_address = None
        data["Email"] = email_address

        data["Public Key"] = crypto_cert.public_key().public_bytes(
            encoding=serialization.
            Encoding.PEM,
            format=serialization.
            PublicFormat.SubjectPublicKeyInfo).decode("ascii")

        try:
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
            issuer = names[0].value
        except x509.ExtensionNotFound:
            issuer = None
        data["Issuer"] = issuer

        # print()

    def should_execute(self, service: str, port: int) -> bool:
        if port == 443:
            return True
        if service == "ssl/https":
            return True
        if service == "https":
            return True
        return False
