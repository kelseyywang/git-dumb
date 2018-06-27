import datetime
import time
import argparse
from os import listdir, makedirs
from os.path import isfile, join, basename, exists

SAVE_FREQ = 600 # Time between saving different versions. Default: 10 min
TIMEOUT = 3600 # Time until program automatically terminates. Default: 1 hr
VERSION_DIRNAME = "versions" # Folder containing version copies
FILES_TO_EXCLUDE = [] # File names to explicitly not copy. Default: none.
IGNORES = [".gitignore"] # File names of files containing file names to explicitly not copy

# To ignore the ignores in the ignore files
def exclude_ignores():
    # Ok why would you even have a gitignore because you're using git-dumb...? Whatever
    for ignore_file in IGNORES:
        with open(ignore_file) as file:
            for line in file:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    FILES_TO_EXCLUDE.append(line)

# Args you can modify include save frequency, timeout amount, and version directory name
def apply_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freq", help="Amount of time between saving new versions (in sec).")
    parser.add_argument("--timeout", help="Amount of time to run until program times out (in sec).")
    parser.add_argument("--dir", help="Name of directory where all versions are stored.")
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

def last_index_of(str, ch):
    for i in range(len(str) - 1, -1, -1):
        if str[i] == ch:
            return i
    return -1

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

def start_dumb_github():
    exclude_ignores()
    apply_args()
    if not exists(VERSION_DIRNAME):
        makedirs(VERSION_DIRNAME)
    start = time.time()
    while time.time() - start < float(TIMEOUT):
        this_filename = basename(__file__)
        # Exclude certain - i.e. myself and hidden files
        all_filenames = [f for f in listdir(".") if isfile(join(".", f)) and f != this_filename and f not in FILES_TO_EXCLUDE and f[0] != '.']
        # Will go through all files contained in this directory. Sorry, you're
        # screwed for now if you make any new directories and put stuff in them hehe
        for filename in all_filenames:
            now = datetime.datetime.now()
            file = open(filename, "r")
            orig_name = filename[0:last_index_of(filename, '.')]
            orig_extension = filename[last_index_of(filename, '.'):]
            version_filename = get_date_str() + "_" + orig_name + orig_extension
            version_file = open(VERSION_DIRNAME + "/" + version_filename, "w+")
            version_file.write(file.read())
            file.close()
            version_file.close()
        time.sleep(int(SAVE_FREQ))

start_dumb_github()
