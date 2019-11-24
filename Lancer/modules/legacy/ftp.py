import ftplib
from core import config, spinner, utils
import io
import sys
import os
import mimetypes


def ftp(open_port):
    if config.args.quiet is not True:
        anonymous_access_allowed = False

        for script in open_port.getElementsByTagName('script'):
            if script.attributes['id'].value == "ftp-anon":
                anonymous_access_allowed = True

        if anonymous_access_allowed:
            print(utils.warning_message(), "Anonymous FTP access allowed")
            ftp_client = ftplib.FTP(config.current_target)
            ftp_client.login()
            download_files(ftp_client)
            ftp_client.quit()
        else:
            print(utils.warning_message(), "Credentials are required for FTP access")
    else:
        print(utils.normal_message(), "Not downloading any files or logging on to server as currently in quiet mode")


def download_files(ftp_client):
    print(utils.normal_message(), "Downloading all files under 50mb into FTP cache...")
    print(utils.warning_message(), "FTP Server banner:", ftp_client.getwelcome()[4:])

    files = get_folder_contents(ftp_client)

    print(utils.warning_message(), len(files), "files found")

    if len(files) > 0:
        sanitised_ftp_files, files_too_large = remove_files_over_size(ftp_client, files)

        print(utils.warning_message(), len(files_too_large), "files over 50mb")
        print(utils.normal_message(), len(sanitised_ftp_files), "files under 50mb")

        if config.args.verbose:
            for large_file in files_too_large:
                file_name, file_ext = os.path.splitext(large_file)
                file_type = mimetypes.guess_type(large_file)[0]
                if file_type is not None:
                    file_type = str(file_type)
                else:
                    file_type = "Unknown - " + file_ext

                print(utils.warning_message(), file_name, "(" + file_type + ") is too large to download")

        for filename in sanitised_ftp_files:
            print(utils.normal_message(), "Downloading", filename, end=' ')
            download_file(ftp_client, filename)
            # Clear the "Downloading..." file line
            sys.stdout.write('\x1b[2K\r')
            sys.stdout.flush()
            print(utils.normal_message(), "Downloaded", filename, "to FTP cache")

        print(utils.normal_message(), "Finished downloading all files under 50mb into FTP cache")
    else:
        print(utils.normal_message(), "No files to download")


def get_folder_contents(ftp_client, path=''):
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
        files_ret = get_folder_contents(ftp_client, os.path.join(path, directory))
        # Add the files in this directory to it
        for file in files_ret:
            files.append(file)

    # Return all of the files we have in the form of their local paths
    return files


def download_file(ftp_client, filename):
    with spinner.Spinner():
        if not os.path.exists(os.path.join(config.ftp_cache(), config.current_target)):
            os.makedirs(os.path.join(config.ftp_cache(), config.current_target))
        local_filename = os.path.join(config.ftp_cache(), config.current_target, filename)

        if not os.path.exists(os.path.dirname(local_filename)):
            os.mkdir(os.path.dirname(local_filename))
        file = open(local_filename, 'wb')
        ftp_client.retrbinary('RETR ' + filename, file.write)
        file.close()


def remove_files_over_size(ftp_client, files, size=1024*1024*50):
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
