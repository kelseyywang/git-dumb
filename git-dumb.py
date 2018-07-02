import datetime
import time
import argparse
from os import listdir, makedirs
from os.path import isfile, join, basename, exists, isdir, normpath

SAVE_FREQ = 1800
TIMEOUT = 10800
VERSION_DIRNAME = "versions"
IGNORES = [".gitignore", ".hgignore"] # File names of files containing file names to explicitly not copy. By default: .gitignore and .hgignore
ignore_list = []

# Process args if passed in
def apply_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freq", help="Amount of time between saving new versions (in sec). Default: 1800 (30 min)")
    parser.add_argument("--timeout", help="Amount of time to run until git-dumb terminates (in sec). Default: 10800 (3 hrs)")
    parser.add_argument("--dir", help="Name of directory where all versions are stored. Default: \"versions\"")
    args = parser.parse_args()
    if args.freq:
        global SAVE_FREQ
        SAVE_FREQ = args.freq
    if args.timeout:
        global TIMEOUT
        TIMEOUT = args.timeout
    if args.dir:
        global VERSION_DIRNAME
        VERSION_DIRNAME = args.dir

# To ignore the ignores in the ignore files ;)
# Returns file paths to exclude
def exclude_ignores():
    excluded_paths = []
    for ignore_file in IGNORES:
        if isfile(ignore_file):
            with open(ignore_file) as file:
                for line in file:
                    line = line.strip()
                    if len(line) > 0 and line[0] != '#' and line not in excluded_paths and (isfile(line) or isdir(line)):
                        excluded_paths.append(normpath(line))
            file.close()
    return excluded_paths

def get_date_str():
    now = datetime.datetime.now()
    month, day, hour, minute, second = (str(now.month), str(now.day), str(now.hour), str(now.minute), str(now.second))
    if len(month) < 2:
        month = "0" + month
    if len(day) < 2:
        day = "0" + day
    if len(hour) < 2:
        hour = "0" + hour
    if len(minute) < 2:
        minute = "0" + minute
    if len(second) < 2:
        second = "0" + second
    return str(now.year) + "-" + month + "-" + day + "_" + hour + "-" + minute + "-" + second

# Copies files/dirs from directory path into corresponding place in backup folder
# Returns date string
def copy_stuff(directory, ignores_from_ignore_file):
    date_str = get_date_str()
    if not exists(join(VERSION_DIRNAME, date_str)):
        makedirs(join(VERSION_DIRNAME, date_str))
    this_filename = basename(__file__)
    all_contents = listdir(directory)
    file_list = []
    dir_list = []
    # Separate all contents of directory in files, directories, and things to ignore
    for c in all_contents:
        full_path = normpath(join(directory, c))
        if isdir(full_path) and full_path != VERSION_DIRNAME and (full_path not in ignores_from_ignore_file) and c[0] != '.':
            dir_list.append(full_path)
        elif isfile(full_path) and full_path != this_filename and (full_path not in ignores_from_ignore_file) and c[0] != '.':
            file_list.append(full_path)
        else:
            ignore_list.append(full_path)
    # Copy files
    for file_path in file_list:
        now = datetime.datetime.now()
        file = open(file_path, "rb")
        version_filename = join(VERSION_DIRNAME, date_str, file_path)
        version_file = open(version_filename, "wb+")
        version_file.write(file.read())
        file.close()
        version_file.close()
    # Copy directories and recursive call within each new directory
    for dir_path in dir_list:
        if not exists(join(VERSION_DIRNAME, date_str, dir_path)):
            makedirs(join(VERSION_DIRNAME, date_str, dir_path))
        copy_stuff(dir_path, ignores_from_ignore_file)
    return date_str

def main():
    apply_args()
    start = time.time()
    global ignore_list
    while time.time() - start <= float(TIMEOUT):
        ignore_list = []
        ignores_from_ignore_file = exclude_ignores()
        date_str = copy_stuff(".", ignores_from_ignore_file)
        print("The following files/directories within in this directory were excluded from the latest backup at " + date_str + ":")
        for c in ignore_list:
            print(c)
        print()
        time.sleep(int(SAVE_FREQ))

if __name__ == "__main__":
    main()
