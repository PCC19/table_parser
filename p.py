import sys
import re
import random

def roll_dice(dice_str):
    match = re.match(r"(\d+)d(\d+)([+-]\d+)?", dice_str)
    if not match:
        return dice_str
    num_dice = int(match.group(1))
    dice_sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    total = sum(random.randint(1, dice_sides) for _ in range(num_dice)) + modifier
    return str(total)

def get_first_line(filename):
    with open(filename, 'r') as f:
        return f.readline().strip()

def replace_dice_rolls(text):
    pattern = r"\d+d\d+([+-]\d+)?"
    replaced = False
    def replacer(match):
        nonlocal replaced
        replaced = True
        return roll_dice(match.group(0))
    new_text = re.sub(pattern, replacer, text)
    return new_text, replaced

def replace_file_patterns(text, first_line):
    replaced = False
    if "[file]" in text:
        text = text.replace("[file]", first_line)
        replaced = True
    pattern = r"\[2d6 file\]"
    matches = re.findall(pattern, text)
    if matches:
        replaced = True
        def replacer(match):
            n = int(roll_dice("2d6"))
            return "\n".join([first_line]*n)
        text = re.sub(pattern, replacer, text)
    return text, replaced

def recursive_parse(text, first_line):
    while True:
        text, replaced_dice = replace_dice_rolls(text)
        text, replaced_file = replace_file_patterns(text, first_line)
        if not (replaced_dice or replaced_file):
            break
    return text

def main():
    if len(sys.argv) < 2:
        print("Usage: python parser.py <file1> <file2> ...")
        sys.exit(1)
    files = sys.argv[1:]
    file_counts = {}
    for filename in files:
        if filename not in file_counts:
            file_counts[filename] = 1
        else:
            file_counts[filename] += 1
        first_line = get_first_line(filename)
        with open(filename, 'r') as f:
            content = f.read()
        parsed_content = recursive_parse(content, first_line)
        output_filename = f"{filename}.{file_counts[filename]}"
        with open(output_filename, 'w') as f:
            f.write(parsed_content)
        print(f"Parsed {filename} -> {output_filename}")

if __name__ == '__main__':
    main()

