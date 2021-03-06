#!/usr/bin/python3

import argparse
import os
from prettytable import PrettyTable


ext_checks = {
    "exec_types": ['.php', '.js', '.cs', '.py', '.java', '.asp', '.aspx', '.jsp', '.ts'],
    "configs": { "extensions": ['.conf', '.json', '.yml', '.yaml', '.cfg', '.ini', '.config', '.cnf'], "located": [] },
    "shells": { "extensions": ['.sh', '.bat'], "located": [] },
    "logs": { "extensions": ['.log'], "located": [] },
    "xml": { "extensions": ['.xml'], "located": [] },
    "db": { "extensions": ['.db', '.mdb', '.sql', '.sqlite', '.db3', '.dbf', '.s3db', '.myd'], "located": [] },
    "hvt": { "extensions": ['user', 'database', 'conf', 'secret', 'config', 'configuration', 'db', 'dockerfile'], "located": [] },
    "investigate": { "extensions": ['.csv', '.bak', '.backup'], "located": [] },
    "interesting_files": {"strings": ['commands', 'cronjobs', 'serviceescalations', 'exec', 'accesstoken']}
}

sql_checks = r".*(sql|query|qry|sequel).*(\+).*"
secrets = [
    'SECRET', 'DJANGO_SECRET', 'SECRET_KEY', 'ENV', '.env', 'API', 'PASS', 'TOKEN', 'DEBUG=True',
    'username', 'password', 'user', 'pass', 'pwd'
    ]

findings =  {
    "type": "",
    "file": "",
    "find_string": "",
    "line": ""
} 

exec_types = {
    "node": {
        "checks": {
            "rce": ["exec", "eval", "spawn"],
            "deserialization": ['serialize', 'deserialize', 'unserialize', "require('cryo')", 'cryo', "require('node-serialize')", 'node-serialize'],
            "secrets": secrets
            },
    },
    "python": {
        "checks": {
            "rce": [ 
                'system', 'check_output', 'popen', 'popen2', 'popen3' 'Popen', 'call', 'communicate', 'run',
                'spawn', 'spawnlp', 'spawnvp', 'spawnlpe', 'getstatusoutput', 'getoutput' 
                ],
            "deserialization": ['pickle', '__reduce'],
            "secrets": secrets
            }
    },
    "dotnet": {
        "checks": {
            "rce": [],
            "deserialization": [],
            "secrets": secrets
            },
    },
    "php": {
        "checks": {
            "rce": [],
            "deserialization": [],
            "secrets": secrets
            },
    },
    "java": {
        "checks": {
            "rce": [],
            "deserialization": [],
            "secrets": secrets
            },
    },
}


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", "-d", help="Start directory to analyse", required=True)
    return parser.parse_args()

def check_extension(ext, f):
    for ex in ext:
        return True if f.lower().endswith(ex) else False

def is_high_value(f):
    for h in ext_checks["hvt"][0]:
        return True if h in f.lower().split('/')[-1] else False

def investigate(f):
    for i in ext_checks["interesting_files"][0]:
        return True if f.lower().endswith(i) else False       


def get_all_files(dir):
    all_files = []
    for dirpath, subdirs, files in  os.walk(dir, topdown=True, onerror=None, followlinks=False):
        for f in files:
            all_files.append(os.path.join(dirpath, f))
    return all_files


def make_table():
    pt = PrettyTable()
    pt.field_names(["ID", "Vuln Class", "File Type", "File Path", "Finding", "Line #"])


def main():
    args = get_args()
    files = get_all_files(args.dir)


if __name__ == "__main__":
    main()
