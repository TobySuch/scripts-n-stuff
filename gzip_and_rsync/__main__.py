import tarfile
import subprocess


def gzip_folder(dest_path, *source_folders):
    with tarfile.open(dest_path, mode='w:gz') as f:
        for path in source_folders:
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
    subprocess.run(command)


if __name__ == "__main__":
    gzip_folder("gzip_and_rsync/out2.tar.gz", "gzip_and_rsync/test_dir/")
    rsync_files("gzip_and_rsync/", "backups", "alibi.pi",
                "~/Test/", source_is_dir=True)
