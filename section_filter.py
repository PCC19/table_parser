#!/usr/bin/python3
import sys
import re

def get_indent(line):
    """Returns the indentation (number of leading spaces or tabs) of a line."""
    return len(line) - len(line.lstrip('\t'))

def section_filter(filename, pattern):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        print("line:", line)
        print(re.search(pattern, line))
        if re.search(pattern, line):
            base_indent = get_indent(line)
            print(line, end='')  # Print the matching line
            i += 1
            # Print all subsequent lines with greater indentation
            while i < len(lines) and get_indent(lines[i]) > base_indent:
                print(lines[i], end='')
                i += 1
        else:
            i += 1

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python section_filter.py <filename> <pattern>")
        sys.exit(1)
    section_filter(sys.argv[1], sys.argv[2])

