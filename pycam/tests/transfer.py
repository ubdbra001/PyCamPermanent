#!/usr/bin/env python

# Script to simulate pycam data transfer

from pathlib import Path
from shutil import copyfile
from time import sleep
from re import findall
import sys

def get_avail_datetimes(source, file_match = "**/*Plume.npy"):
    """Get a list of all available unique datetimes"""
    # Look in dir and list all spec (npy) files
    spec_files = source.glob(file_match)
    # Extract datetimes from those spec files
    dtimes = [findall(r"\d{4}-\d{2}-\d{2}T\d{6}", fname.as_posix())[0]
              for fname in spec_files]
    return dtimes

def get_files(source, dtime):
    """Get a list of files that contain a specific datetime"""
    return source.glob("**/*" + dtime + "*Plume*")

def transfer_data(source, dest, delay = 5):
    """
    Copies data from source to dest with a user-defined pause between sets of
    files with different date/times in filename
    """
    dtimes = get_avail_datetimes(source)
    for dtime in dtimes:
        files_gen = get_files(source, dtime)
        for file in files_gen:
            file_loc = file.relative_to(source)
            file_dest = dest.joinpath(file_loc)
            lock_path = create_lock(file_dest)
            copyfile(file, file_dest)
            remove_lock(lock_path)

            print(file_loc, ": ", source,  " -> ", file_dest, sep = None)
            
        print('\r')
        sleep(delay)

def clear_dest(dest):
    """
    Makes sure the dest directory is empty before transfer
    """
    [file.unlink() for file in dest.iterdir() if file.is_file()]

def create_lock(file_path):
    """
    Creates lock file to ensure that file being transferred is not accessed until fully available
    """
    lock_path = file_path.with_suffix(".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "w") as file:
        pass

    return lock_path

def remove_lock(file_path):
    """
    Removes lock file once file has finished copying
    """
    file_path.unlink()

if __name__ == '__main__':
    source = Path(sys.argv[1])
    dest = Path(sys.argv[2])
    delay = float(sys.argv[3])

    try:
        transfer_data(source, dest, delay)
    except KeyboardInterrupt:
        clear_dest(dest)
        print("Cleared up and finished")

