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

        self.logger.info("Starting SSL Certificate Extraction...")

        self.logger.debug("Encoding target IP/hostname")
        hostname_idna = idna.encode(ip)
        self.logger.debug("Successfully encoded target IP/hostname".format(IP=ip, PORT=port))
        sock = socket.socket()
        self.logger.debug("Connecting to {IP}:{PORT}".format(IP=ip, PORT=port))
        sock.connect((ip, port))
        self.logger.debug("Connecting to {IP}:{PORT}".format(IP=ip, PORT=port))
        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)  # most compatible
        ctx.check_hostname = False
        ctx.verify_mode = OpenSSL.SSL.VERIFY_NONE

        sock_ssl = OpenSSL.SSL.Connection(ctx, sock)
        sock_ssl.set_connect_state()
        sock_ssl.set_tlsext_host_name(hostname_idna)
        try:
            self.logger.debug("Negotiating SSL handshake with {IP}:{PORT}".format(IP=ip, PORT=port))
            sock_ssl.do_handshake()
            self.logger.info("Negotiated SSL handshake with {IP}:{PORT}".format(IP=ip, PORT=port))
        except OpenSSL.SSL.Error:
            # TODO: Don't quietly return
            self.logger.error("Unable to negotiate SSL2/3 handshake with server")
            return
        cert = sock_ssl.get_peer_certificate()
        crypto_cert = cert.to_cryptography()
        sock_ssl.close()
        sock.close()
        self.logger.debug("Retrieved SSL certificate from {IP}:{PORT}".format(IP=ip, PORT=port))

        # Now we've got the SSL cert, create the SSL certificate components
        self.create_loot_space(ip=ip, port=port)

        data = Loot.loot[ip][str(port)][self.loot_name]

        try:
            self.logger.debug("Getting SSL Common Name")
            names = crypto_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
            common_name = names[0].value
            self.logger.debug("Successfully retrieved SSL Common Names")
        except x509.ExtensionNotFound:
            common_name = None
            self.logger.debug("Unable to get SSL Common Name")
        except IndexError:
            common_name = None
            self.logger.debug("Unable to get SSL Common Name")
        data["Common Name"] = common_name

        try:
            self.logger.debug("Getting SSL Alternative Names")
            ext = crypto_cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
            alt_names = ext.value.get_values_for_type(x509.DNSName)
            self.logger.debug("Successfully retrieved SSL Alternative Names")
        except x509.ExtensionNotFound:
            alt_names = None
            self.logger.debug("Unable to get SSL Alternative Names")
        data["Alt Names"] = alt_names

        data["Issue Date"] = str(crypto_cert.not_valid_before)
        data["Expiry Date"] = str(crypto_cert.not_valid_after)

        expired = crypto_cert.not_valid_after < datetime.datetime.now()

        data["Expired"] = expired

        try:
            self.logger.debug("Getting SSL Country")
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.COUNTRY_NAME)
            country_name = names[0].value
            self.logger.debug("Successfully retrieved SSL Country")
        except x509.ExtensionNotFound:
            country_name = None
            self.logger.debug("Unable to get SSL Country")
        data["Country"] = country_name

        try:
            self.logger.debug("Getting SSL State/Provice")
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)
            province_name = names[0].value
            self.logger.debug("Successfully retrieved SSL State/Provice")
        except x509.ExtensionNotFound:
            province_name = None
            self.logger.debug("Unable to get SSL State/Provice")
        except IndexError:
            province_name = None
            self.logger.debug("Unable to get SSL State/Provice")
        data["Province"] = province_name

        try:
            self.logger.debug("Getting SSL Locality")
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.LOCALITY_NAME)
            locality_name = names[0].value
            self.logger.debug("Successfully retrieved SSL Locality")
        except x509.ExtensionNotFound:
            locality_name = None
            self.logger.debug("Unable to get SSL Locality")
        except IndexError:
            locality_name = None
            self.logger.debug("Unable to get SSL Locality")
        data["Locality"] = locality_name

        try:
            self.logger.debug("Getting SSL Organisation Name")
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)
            organization_name = names[0].value
            self.logger.debug("Successfully retrieved SSL Organisation Name")
        except x509.ExtensionNotFound:
            organization_name = None
            self.logger.debug("Unable to get SSL Organisation Name")
        data["Organisation Name"] = organization_name

        try:
            self.logger.debug("Getting SSL Organisation Unit Name")
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)
            organizational_unit_name = names[0].value
            self.logger.debug("Successfully retrieved SSL Organisation Unit Name")
        except x509.ExtensionNotFound:
            organizational_unit_name = None
            self.logger.debug("Unable to get SSL Organisation Unit Name")
        except IndexError:
            organizational_unit_name = None
            self.logger.debug("Unable to get SSL Organisation Unit Name")
        data["OU"] = organizational_unit_name

        try:
            self.logger.debug("Getting SSL Email Address")
            emails = crypto_cert.issuer.get_attributes_for_oid(NameOID.EMAIL_ADDRESS)
            email_address = emails[0].value
            self.logger.debug("Successfully retrieved SSL Email Address")
        except x509.ExtensionNotFound:
            email_address = None
            self.logger.debug("Unable to get SSL Email Address")
        except IndexError:
            email_address = None
            self.logger.debug("Unable to get SSL Email Address")
        data["Email"] = email_address

        data["Public Key"] = crypto_cert.public_key().public_bytes(
            encoding=serialization.
            Encoding.PEM,
            format=serialization.
            PublicFormat.SubjectPublicKeyInfo).decode("ascii")

        try:
            self.logger.debug("Getting SSL certificate issuer")
            names = crypto_cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
            issuer = names[0].value
            self.logger.debug("Successfully retrieved SSL certificate issuer")
        except x509.ExtensionNotFound:
            issuer = None
            self.logger.debug("Unable to get SSL certificate issuer")
        data["Issuer"] = issuer

        self.logger.info("Successfully extracted SSL Certificate information")

    def should_execute(self, service: str, port: int) -> bool:
        if port == 443:
            return True
        if service == "ssl/https":
            return True
        if service == "https":
            return True
        return False
