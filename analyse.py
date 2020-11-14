#!/usr/bin/python3

import argparse
import os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", "-d", help="Start directory to analyse", required=True)
    return parser.parse_args()


def is_config_file(f):
    return True if f.lower().endswith(
        '.conf', '.json', '.yml', '.yaml', '.cgf', '.ini', '.config'
        ) else False

def is_shell_script(f):
    return True if f.lower().endswith('.sh') else False

def is_batch_script(f):
    return True if f.lower().endswith('.bat') else False

def is_log_file(f):
    return True if f.lower().endswith('.log') else False

def is_xml_file(f):
    return True if f.lower().endswith('.xml') else False

def is_high_value(f):
    hvt = ['user', 'database', 'configuration', 'db', 'password']
    return any(hvt in f.lower())          


def get_all_files(dir):
    all_files = []
    for dirpath, subdirs, files in  os.walk(dir, topdown=True, onerror=None, followlinks=False):
        for f in files:
            all_files.append(os.path.join(dirpath, f))
    return all_files


def main():
    args = get_args()
    get_all_files(args.dir)


if __name__ == "__main__":
    main()
