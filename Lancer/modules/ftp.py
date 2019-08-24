import ftplib
import config
import io
import utils
import sys
import spinner
import os


def ftp(open_port):
    if config.args.quiet is not True:
        anonymous_access_allowed = False

        for script in open_port.getElementsByTagName('script'):
            if script.attributes['id'].value == "ftp-anon":
                anonymous_access_allowed = True

        if anonymous_access_allowed:
            print(utils.warning_message(), "Anonymous FTP access allowed")
            ftp_client = ftplib.FTP(config.args.target)
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
        sanitised_ftp_files = remove_files_over_size(ftp_client, files)
        print(utils.normal_message(), len(sanitised_ftp_files), "files under 50mb")

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

    captured_output = io.StringIO()
    sys.stdout = captured_output
    ftp_client.dir(path)
    sys.stdout = sys.__stdout__
    directory_listing = captured_output.getvalue().splitlines()

    # Right, a little explanation for how we parse the files and directories
    # Every single file listing is in this format:
    # drwxr-xr-x 1 ftp ftp              0 Aug 24 12:52 Backups
    # -r--r--r-- 1 ftp ftp       20971520 Aug 21 19:25 TestFile.zip
    # A colon only occurs once: and that is three characters before the
    # start of the file name. Therefore, we split at the colon and substring
    # from the fourth character (the start of the file/directory name) to the end

    # TODO: Further testing needed
    for file in directory_listing:
        if ':' in file:
            if file[0] == 'd':
                directory_name = ' '.join(file.split(':')[-1:])[3:]
                directories.append(directory_name)
            else:
                file_name = ' '.join(file.split(':')[-1:])[3:]
                print(utils.normal_message(), "Located", file_name)
                file_path = os.path.join(path, file_name)
                files.append(file_path)
        else:
            print(utils.error_message(), "Unable to parse directory listing of file", file)

    for directory in directories:
        files_ret = get_folder_contents(ftp_client, os.path.join(path, directory))
        for file in files_ret:
            files.append(file)

    return files


def download_file(ftp_client, filename):
    with spinner.Spinner():
        # TODO: Make ftp directory selectable
        if not os.path.exists(os.path.join(config.ftp_cache(), config.args.target)):
            os.makedirs(os.path.join(config.ftp_cache(), config.args.target))
        local_filename = os.path.join(config.ftp_cache(), config.args.target, filename)
        if not os.path.exists(os.path.dirname(local_filename)):
            os.mkdir(os.path.dirname(local_filename))
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
            print(utils.warning_message(), "Don't have permission to access", utils.color(file, None, None, "bold") + ",",
                  "could be a directory or a file we don't have permission to access")
    return sanitised_files
