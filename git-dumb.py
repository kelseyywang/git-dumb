import datetime
import time
import argparse
from os import listdir, makedirs
from os.path import isfile, join, basename, exists, isdir

SAVE_FREQ = 600 # Time between saving different versions. Default: 10 min
TIMEOUT = 3600 # Time until program automatically terminates. Default: 1 hr
VERSION_DIRNAME = "versions" # Folder containing version copies
FILES_TO_EXCLUDE = [] # File names of files to explicitly not copy. Default: none.
IGNORES = [".gitignore"] # File names of files containing file names to explicitly not copy

# To ignore the ignores in the ignore files ;)
def exclude_ignores():
    for ignore_file in IGNORES:
        if isfile(ignore_file):
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

def copy_stuff(directory):
    date_str = get_date_str()
    if not exists(join(VERSION_DIRNAME, date_str)):
        makedirs(join(VERSION_DIRNAME, date_str))
    this_filename = basename(__file__)
    all_contents = listdir(directory)
    file_list = []
    dir_list = []
    ignore_list = [] #TODO: print at end
    for c in all_contents:
        if isdir(join(directory, c)) and c[0] != '.' and c != VERSION_DIRNAME:
            dir_list.append(c)
        elif isfile(join(directory, c)) and c != this_filename and c not in FILES_TO_EXCLUDE and c[0] != '.':
            file_list.append(c)
        else:
            ignore_list.append(c)
    for filename in file_list:
        now = datetime.datetime.now()
        file = open(join(directory, filename), "r")
        version_filename = join(VERSION_DIRNAME, date_str, directory, filename)
        version_file = open(version_filename, "w+")
        version_file.write(file.read())
        file.close()
        version_file.close()
    for newdir in dir_list:
        if not exists(join(VERSION_DIRNAME, date_str, directory, newdir)):
            makedirs(join(VERSION_DIRNAME, date_str, directory, newdir))
        copy_stuff(join(directory, newdir))

def start_dumb_github():
    exclude_ignores()
    apply_args()
    start = time.time()
    while time.time() - start + float(SAVE_FREQ) <= float(TIMEOUT):
        copy_stuff(".")
        time.sleep(int(SAVE_FREQ))
        
start_dumb_github()
