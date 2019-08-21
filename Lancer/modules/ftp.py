from utils import *

import ftplib
import config


def ftp(open_port):
    if config.args.quiet is not True:
        for script in open_port.getElementsByTagName('script'):
            if script.attributes['id'].value == "ftp-anon":
                print(warning_message(), "Anonymous FTP access allowed")
                ftp_client = ftplib.FTP(config.args.target)
                ftp_client.login()
                download_files(ftp_client)
                ftp_client.quit()
    else:
        print(normal_message(), "Not downloading any files or logging on to server as currently in quiet mode")


def download_files(ftp_client):
    print(normal_message(), "Downloading all files under 100mb into ./ftp/" + config.args.target + "...")

    print(warning_message(), "FTP Server banner:", ftp_client.getwelcome()[4:])

    ftp_files = ftp_client.nlst()
    print(warning_message(), len(ftp_files), "files found")

    if len(ftp_files) > 0:
        sanitised_ftp_files = remove_files_over_size(ftp_client, ftp_files)
        print(normal_message(), len(sanitised_ftp_files), "files under 50mb")

        for filename in sanitised_ftp_files:
            print(normal_message(), "Downloading", filename, end=' ')
            download_file(ftp_client, filename)
            # Clear the "Downloading..." file line
            sys.stdout.write('\x1b[2K\r')
            sys.stdout.flush()
            print(normal_message(), "Downloaded", filename, "to ./ftp/" + config.args.target)

        print(normal_message(), "Finished downloading all files under 50mb into ./ftp/")
    else:
        print(normal_message(), "No files to download")


def download_file(ftp_client, filename):
    with Spinner():
        # TODO: Make ftp directory selectable
        if not os.path.exists(os.path.join("ftp", config.args.target)):
            os.makedirs(os.path.join("ftp", config.args.target))
        local_filename = os.path.join(os.path.join('ftp', config.args.target), filename)
        file = open(local_filename, 'wb')
        ftp_client.retrbinary('RETR ' + filename, file.write)
        file.close()


def remove_files_over_size(ftp_client, files, size=1024*1024*50):
    sanitised_files = []
    for file in files:
        try:
            # If the file is smaller than 50MiB
            if ftp_client.size(file) < size:
                sanitised_files.append(file)
        except ftplib.error_perm:
            print(warning_message(), "Don't have permission to access", color(file, None, None, "bold") + ",",
                  "could be a directory or a file we don't have permission to access")
    return sanitised_files
