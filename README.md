# Sorter

## What does it do?

Script analyzes contents of provided directory and moves all files found to extension based folders in parent directory.

## Example

![sorter.py_example](/mess%20inside/mess2/test1/Sorter_demo.gif)

## Usage

In command line type:

`python sorter.py`

You will be prompted for a directory you are willing to sort. If you provide invalid path or simply hit Enter, path, where sorter.py file is present will be sorted.

**Note: there's no turning back from here.**

If want to output log file including tree structures and code progress, type `python sorter.py log_file`. By default sorter.py logs messages to terminal. Check repository for example log file: [sorter.log](sorter.log)

### Features

* Optional logging to a file;
* Outputs folder tree structure before and after file sorting (log file / terminal);
* prevents sorting of absolute path, if it includes any of the following list items: `['windows', 'program files', 'bin', 'lib', 'etc', 'applications']`;
* handles duplicate files: same filename - different content / two copies of same file in different directories;
* handles files with increased permissions (needs more testing).

## Requirements
Python 3.7.3+ All libraries used in this project are within Python's standard library.

## Additional notes

Script was mainly written for learning purposes on navigating OS and getting a handle on python `OS` library

