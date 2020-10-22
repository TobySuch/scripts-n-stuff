import shutil, glob, argparse, re, os
from pathlib import Path

# {'jpeg', 'json', 'gif', 'mkv', 'MOV', 'jpg', 'JPG', 'mp4', 'mov', 'PNG', 'webp', 'png'}


def clean_path(path):
    """
    Cleans the path to allow it to be used to search with glob.

    It does a few different things:
    - Replaces ~ with the users home directory.
    - Makes sure the path ends with a /

    param: path: The path to clean.
    returns: The cleaned path.
    """
    path = path.replace("~", str(Path.home()))
    if path[-1] != "/":
        path += "/"
    return path

def get_path_names(directory):
    """Gets a list of all the paths within the given directory"""
    paths_without_source = set()
    paths = glob.glob(source + "**/*.*", recursive=True)
    for p in paths:
        paths_without_source.add(p.replace(directory, "", 1))

    return paths_without_source


def include_filter(incl_filter, paths):
    """
    Matches a set of paths against an include filter.

    param: incl_filter: The filter to match.
    param: paths: The set of paths to match against the filter.
    returns: A set of paths which match the include filter.
    """
    hits = set()
    for p in paths:
        if re.search(incl_filter, p):
            hits.add(p)

    return hits

def exclude_filter(excl_filter, paths):
    """
    Matches a set of paths against an exclude filter, removing those that don't match

    param: excl_filter: The filter to match.
    param: paths: The set of paths to match against the filter.
    returns: A set of paths which do not match the filter.
    """
    misses = set()
    for p in paths:
        if re.search(excl_filter, p) is None:
            misses.add(p)

    return misses

def run_filters(incl_filters, excl_filters, paths):
    """Runs the paths against the filters

    Keeps any path which matches any include filter but also does not match any
    exlude paths.

    param: incl_filters: The include filters.
    param: excl_filters: The exclude filters.
    param: paths: The paths to match against the filters.
    returns: A set of paths which match the filters.
    """
    # Run include filters
    if incl_filters:
        incl_paths = set()
        for incl_filt in incl_filters:
            ps = include_filter(incl_filt, paths)
            incl_paths = incl_paths.union(ps)
    else:
        incl_paths = paths

    # Run exclude filters
    if excl_filters:
        for excl_filt in excl_filters:
            incl_paths = exclude_filter(excl_filt, incl_paths)

    return incl_paths

def flatten_path(path):
    """Returns the file name in the path without the directory before"""
    return path.split("/")[-1]

def copy_file(source, destination, path, flatten=False):
    """
    Copies a file in source to destination.

    Copies a file which may be in a subdirectory from source to destination.
    If flatten is true then the file will not keep its sub directory in the 
    destination.
    param: source: The source directory to find the file.
    param: destination: The destination directory for the file.
    param: path: The path from the source directory to find the file.
    param: flatten: If true then the full path from source to file is not kept
                    in the destination directory.
    returns: None
    """
    source_path = source + path
    if flatten:
        destination_path = destination + flatten_path(path)
    else:
        destination_path = destination + path
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    shutil.copy2(source_path, destination_path)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    Source: https://stackoverflow.com/a/34325723/10302137
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively copy files from a"
                                     + " directory that match a filter to "
                                     + "another directory.")

    parser.add_argument("SOURCE", help="The directory to copy from.")
    parser.add_argument("DESTINATION", help="The directory to copy to.")

    parser.add_argument("-i", "--include", action="append",
                        help="Regex filter to include. Any path which does not "
                             + "match any include filter will be ignored.")

    parser.add_argument("-e", "--exclude", action="append",
                        help="Regex filter to exclude. Any path which matches "
                             + "any exclude filter will be ignored.")

    parser.add_argument("--flatten", action="store_true", 
        help="If set, during the copy all the files will be placed in the "
        + "destination directory, with no sub folders. Otherwise the original "
        + "sub folder structure will be replicated in the destination.")

    args = parser.parse_args()

    source = clean_path(args.SOURCE)
    destination = clean_path(args.DESTINATION)

    paths = get_path_names(source)

    paths = run_filters(args.include, args.exclude, paths)

    number_of_paths = len(paths)
    for i, path in enumerate(paths):
        copy_file(source, destination, path, flatten=args.flatten)
        printProgressBar(i+1, number_of_paths, prefix='Progress:', suffix='Complete')



    