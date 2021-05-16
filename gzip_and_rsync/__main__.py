import tarfile


def gzip_folder(dest_path, *source_folders):
    with tarfile.open(dest_path, mode='w:gz') as f:
        for path in source_folders:
            f.add(path)


if __name__ == "__main__":
    gzip_folder("gzip_and_rsync/out2.tar.gz", "gzip_and_rsync/test_dir")
