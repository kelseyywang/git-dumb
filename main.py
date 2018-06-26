import datetime
import time
from os import listdir, makedirs
from os.path import isfile, join, basename, exists

# Play around with numbers depending on how many messy files you want!1!!1
SAVE_FREQ = 600 # Default: save every 600 sec = 10 min
TIME_ACTIVE = 3600 # Default: this "version control" will time out after 3600 sec = 1 hr
VERSION_DIRNAME = "versions" # Default: folder containing version copies is called versions
FILES_TO_EXCLUDE = ["README.md"] # Default: exclude readme

def last_index_of(str, ch):
    for i in range(len(str) - 1, -1, -1):
        if str[i] == ch:
            return i
    return -1
    
def return_date_str():
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
    if not exists(VERSION_DIRNAME):
        makedirs(VERSION_DIRNAME)
    start = time.time()
    while time.time() - start < TIME_ACTIVE:
        this_filename = basename(__file__)
        # Exclude certain files... especially myself and hidden ones
        all_filenames = [f for f in listdir(".") if isfile(join(".", f)) and f != this_filename and f not in FILES_TO_EXCLUDE and f[0] != '.']
        # Will go through all files contained in this directory. Sorry, you're 
        # screwed for now if you make any new directories and put stuff in them hehe
        for filename in all_filenames:
            now = datetime.datetime.now()
            file = open(filename, "r")
            orig_name = filename[0:last_index_of(filename, '.')]
            orig_extension = filename[last_index_of(filename, '.'):]
            version_filename = return_date_str() + "_" + orig_name + orig_extension
            version_file = open(VERSION_DIRNAME + "/" + version_filename, "w+")
            version_file.write(file.read())
            file.close()
            version_file.close()
        time.sleep(SAVE_FREQ)

start_dumb_github()