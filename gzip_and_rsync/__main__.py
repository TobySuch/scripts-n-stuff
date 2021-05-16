import tarfile
import subprocess
import configparser
import datetime
import logging
import sys


def gzip_folders(dest_path, *source_folders):
    with tarfile.open(dest_path, mode='w:gz') as f:
        for path in source_folders:
            logging.debug(f"Adding {path} to tar")
            f.add(path)
    return f


def rsync_files(source_path, rsync_username, rsync_hostname, dest_path,
                source_is_dir=False):
    command = [
        "rsync", source_path,
        f"{rsync_username}@{rsync_hostname}:{dest_path}"
    ]

    if source_is_dir:
        command.append("-r")
    logging.debug(f"rsync command: {' '.join(command)}")
    subprocess.run(command)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        config_path = sys.argv[1]
    else:
        config_path = "config.cfg"

    config = configparser.ConfigParser()
    config.read(config_path)
    log_file = config.get("General", "log_file")
    log_level = config.get("General", "log_level").upper()

    log_level_e = getattr(logging, log_level.upper())

    logging.basicConfig(filename=log_file, level=log_level_e, format='%(asctime)s %(message)s')

    paths = config.get("GZIP", "paths").strip().splitlines()
    temp_path = config.get("GZIP", "temp_path")
    backup_file_name = config.get("GZIP", "backup_file_name")

    export_name = temp_path + datetime.datetime.now().strftime(
        backup_file_name)

    logging.info(f"Creating temporary backup file: {export_name}")
    gzip_folders(export_name, *paths)
    logging.info("Created temporary file.")

    user = config.get("RSYNC", "user")
    host = config.get("RSYNC", "host")
    path = config.get("RSYNC", "dest_path")

    if config.get("RSYNC", "include_previous").lower() == "true":
        rsync_source_path = temp_path
        is_dir = True

    else:
        rsync_source_path = export_name
        is_dir = False

    rsync_files(rsync_source_path, user, host, path, source_is_dir=is_dir)
