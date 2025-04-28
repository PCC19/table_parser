#!/usr/bin/python3
import sys
import re

def get_indent(line):
    """Returns the indentation (number of leading spaces or tabs) of a line."""
    return len(line) - len(line.lstrip('\t'))

def section_filter(lines, pattern):
    i = 0
    output_string = list() 
    while i < len(lines):
        line = lines[i]
        if re.match(pattern+'$', line):
            base_indent = get_indent(line)
            i += 1
            # Print all subsequent lines with greater indentation
            while i < len(lines) and get_indent(lines[i]) > base_indent:
                output_string = output_string + list(lines[i][1:])
                i += 1
        else:
            i += 1
    return output_string

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python section_filter.py <filename> <pattern>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    out = lines
    for args in sys.argv[2:]:
        filtrado = section_filter(out, args)
        out = "".join(filtrado).splitlines('\n')
    print("".join(out))
