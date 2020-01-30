#!/usr/bin/python3
# Requires below files from https://github.com/notracking/hosts-blocklists:
# - domains.txt
# - hostnames.txt

import sys
import argparse
from pathlib import Path

# Some defaults.
default_domains = './hosts-blocklists/domains.txt'
default_hostnames = './hosts-blocklists/hostnames.txt'
default_output = './blackhost-list.conf'

def isfilesexists(input_files):
    for filename, separator in input_files:
        # Check file existance only, ignore "separator".
        try:
            Path(filename).resolve(strict=True)
        except Exception as e:
            print(e)

def strip2fqdn(separator, lines):
    fqdns = []
    for line in lines:
        if not line.startswith('#'):
            line = line.strip().split(separator, 2)
            if line:
                fqdns.append(line[1])
    return fqdns

def syntax2unbound(raw_fqdns):
    # "Set" is like a list but no duplicates, using it to remove dups.
    #fqdns = sorted(set(raw_fqdns))
    fqdns = set(raw_fqdns)
    lines = []
    for fqdn in fqdns:
        local_zone = 'local-zone: "' + fqdn + '" redirect'
        local_data = 'local-data: "' + fqdn + ' A 127.0.0.1"'
        lines.append(local_zone)
        lines.append(local_data)
    return lines

def write2file(lines):
    with open(args.output_file, 'w') as parsed_file:
        for line in lines:
            parsed_file.write(line + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--domains-file', default=default_domains, required=False)
    parser.add_argument('-ih', '--hostnames-file', default=default_hostnames, required=False)
    parser.add_argument('-o', '--output-file', default=default_output, required=False)
    args = parser.parse_args()

    # Add more files for parsing here, see strip2fqdn() & syntax2unbound() for parsing.
    input_files = [
        [args.domains_file, '/'],
        [args.hostnames_file, ' '],
        ]
    isfilesexists(input_files)

    lines = []
    for input_file in input_files:
        path = input_file[0]
        separator = input_file[1]
        with open(path, 'r') as blocklist:
            lines += syntax2unbound(strip2fqdn(separator, blocklist.readlines()))
    write2file(lines)
