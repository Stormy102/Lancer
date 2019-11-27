# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""
from modules.BaseModule import BaseModule
from core.spinner import Spinner
from core import config, utils, Loot

import ftplib
import io
import sys
import os
import socket
import mimetypes


class FTPAnonymousAccess(BaseModule):
    def __init__(self):
        super(FTPAnonymousAccess, self).__init__(name="FTP Anonymous Access",
                                                 description="Enumerates an Anonymous access",
                                                 loot_name="Anonymous FTP Download",
                                                 multithreaded=False,
                                                 intrusive=True,
                                                 critical=False)

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)
        try:
            ftp_client = ftplib.FTP()
            self.logger.debug("Connecting to {IP}:{PORT}".format(IP=ip, PORT=port))
            ftp_client.connect(ip, port)
            self.logger.info("Successfully connected to {IP}:{PORT}".format(IP=ip, PORT=port))
            self.logger.debug("Attempting to login anonymously")
            ftp_client.login()
            self.logger.info("Successfully logged in anonymously to {IP}:{PORT}".format(IP=ip, PORT=port))
            self.logger.debug("Starting to downloading files under 50mb from {IP}:{PORT}".format(IP=ip, PORT=port))
            self.download_files(ftp_client, Loot.loot[ip][str(port)][self.loot_name])
            self.logger.info("Finished downloading files under 50mb from {IP}:{PORT}".format(IP=ip, PORT=port))
            ftp_client.quit()
            self.logger.debug("Disconnected from {IP}:{PORT}".format(IP=ip, PORT=port))
        except socket.gaierror:
            # Log of some kind
            self.logger.error("Failed to connect: Invalid IP Address/Hostname")
        except ConnectionRefusedError:
            # Log of some kind
            self.logger.error("Failed to connect: Connection refused")
        except TimeoutError:
            # Log of some kind
            self.logger.error("Failed to connect: Connection timed out")

    def download_files(self, ftp_client, dictionary: dict):
        files = self.get_folder_contents(ftp_client)

        self.logger.info("{FILE_COUNT} files found".format(FILE_COUNT=len(files)))

        if len(files) > 0:
            dictionary["Files"] = []
            for filename in files:
                dictionary["Files"].append(filename)
            # TODO: Customise file size limit instead of defaulting to 50mb
            sanitised_ftp_files, files_too_large = self.remove_files_over_size(ftp_client, files)

            self.logger.info("{FILE_COUNT} file(s) under 50mb".format(FILE_COUNT=len(sanitised_ftp_files)))
            self.logger.info("{FILE_COUNT} file(s) bigger or equal to 50mb".format(FILE_COUNT=len(files_too_large)))

            for large_file in files_too_large:
                file_name, file_ext = os.path.splitext(large_file)
                file_type = mimetypes.guess_type(large_file)[0]
                if file_type is not None:
                    file_type = str(file_type)
                else:
                    file_type = "Unknown Python mimetype - extension {EXT}".format(EXT=file_ext)
                self.logger.debug("{FILE} ({TYPE}) too big to download".format(FILE=file_name + file_ext,
                                                                               TYPE=file_type))

            dictionary["Downloaded Files"] = []
            for filename in sanitised_ftp_files:
                self.logger.debug("Downloading {FILE} ".format(FILE=filename))
                dictionary["Downloaded Files"].append(filename)

                # print(utils.normal_message(), "Downloading", filename, end=' ')
                # self.download_file(ftp_client, filename)
                # Clear the "Downloading..." file line
                # sys.stdout.write('\x1b[2K\r')
                # sys.stdout.flush()
                self.logger.info("Downloaded {FILE} to FTP cache".format(FILE=filename))

            # print(utils.normal_message(), "Finished downloading all files under 50mb into FTP cache")
        else:
            self.logger.info("No files to download")

    def get_folder_contents(self, ftp_client, path=''):
        directories = []
        files = []

        # Right, a little explanation for how we parse the files and directories
        # Every single file listing is in this format:
        # drwxr-xr-x 1 ftp ftp              0 Aug 24 12:52 Backups
        # -r--r--r-- 1 ftp ftp       20971520 Aug 21       TestFile.zip
        captured_output = io.StringIO()
        sys.stdout = captured_output
        ftp_client.dir(path)
        sys.stdout = sys.__stdout__
        directory_listing = captured_output.getvalue().splitlines()

        known_directories = []
        # If the output starts with a d, we know its a directory. So loop through
        # all of the lines in the output and add them to the list
        for directory in directory_listing:
            if directory.startswith("d", 0, 9):
                known_directories.append(directory)

        # Loop through everything returned in an NLIST command
        # This gives us all of the entries - including directories
        for file in ftp_client.nlst(path):
            in_dir_list = False

            for directory in known_directories:
                # Extract just the file name, as that's
                # all the dir command outputs
                if directory.endswith(os.path.basename(file)):
                    in_dir_list = True

            # If this file is in the directory list, add
            # it to the list of directories
            if in_dir_list:
                directories.append(os.path.basename(file))
            # Otherwise add it to the list of files
            else:
                files.append(file)

        # Iterate through every subdirectory
        for directory in directories:
            # Recursively get the list of files
            files_ret = self.get_folder_contents(ftp_client, os.path.join(path, directory))
            # Add the files in this directory to it
            for file in files_ret:
                files.append(file)

        # Return all of the files we have in the form of their local paths
        return files

    def download_file(self, ftp_client, filename):
        with Spinner():
            if not os.path.exists(os.path.join(config.ftp_cache(), config.current_target)):
                os.makedirs(os.path.join(config.ftp_cache(), config.current_target))
            local_filename = os.path.join(config.ftp_cache(), config.current_target, filename)

            if not os.path.exists(os.path.dirname(local_filename)):
                os.mkdir(os.path.dirname(local_filename))
            file = open(local_filename, 'wb')
            ftp_client.retrbinary('RETR ' + filename, file.write)
            file.close()

    def remove_files_over_size(self, ftp_client, files, size=1024 * 1024 * 50):
        sanitised_files = []
        large_files = []
        for file in files:
            try:
                # If the file is smaller than 50MiB
                if ftp_client.size(file) < size:
                    sanitised_files.append(file)
                else:
                    large_files.append(file)
            except ftplib.error_perm:
                print(utils.warning_message(), "Don't have permission to access", utils.color(file, None, None, "bold")
                      + ",", "could be a directory or a file we don't have permission to access")
        return sanitised_files, large_files

    def should_execute(self, service: str, port: int) -> bool:
        # TODO:
        # if not super(FTPAnonymousAccess, self).should_execute(service, port):
        #     return False
        if service is "ftp":
            return True
        if port is 21:
            return True
        return False
