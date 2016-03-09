#!/usr/bin/env python3
"""Compress Stata data files, if old and big enough.
"""

import os
import zipfile
import time
import sys


def find_tuple(path, extension='dta'):
    """returns files within path and matching extension"""
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.' + extension):
                result.append((root, file))
    return result


def query_yes_no(question):
    """ask y/n question via input() and return their answer"""
    valid = {'y': True, 'n': False}
    while True:
        sys.stdout.write(question + ' [Y/n] ')
        choice = input().lower()
        if choice == '':
            return True
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'y' or 'n'.\n")


def arquive_files(tuple_list, days=90, lmsize=50):
    """arquives files: only those big enough and old enough"""
    for atuple in tuple_list:
        file = os.path.join(atuple[0], atuple[1])
        access_time = os.stat(file).st_atime
        access_time_prsd = time.strptime(time.ctime(os.stat(file).st_atime))
        now = time.time()
        msize = os.stat(file).st_size / (1000**2)
        question = 'File ' + atuple[1] + ' hasn\'t been accessed since ' + \
            time.strftime("%d %b %Y", access_time_prsd) + ' and is ' + \
            "{0:.2f}".format(msize) + ' MB. Arquive?'
        if access_time > now - 60 * 60 * 24 * days:
            continue
        elif msize < lmsize:
            continue
        elif query_yes_no(question):
            os.chdir(atuple[0])
            zf = zipfile.ZipFile(atuple[1] + '.zip', mode='w')
            try:
                zf.write(atuple[1])
            finally:
                zf.close()
                if zipfile.is_zipfile(atuple[1] + '.zip'):
                    os.remove(atuple[1])


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        dtas = find_tuple(arg)
        arquive_files(dtas)
