import random
import sys
import re

def roll_dice(dice_str):
    match = re.match(r"(\d+)d(\d+)([+-]\d+)?", dice_str)
    if not match:
        return dice_str
    num_dice = int(match.group(1))
    dice_sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    total = sum(random.randint(1, dice_sides) for _ in range(num_dice)) + modifier
    return str(total)

def get_item(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return random.choice(lines).strip()

def recursive_parse(text, file_path):
    def replace_match(match):
        prefix = match.group(1)
        if prefix:
            n = roll_dice(prefix)
            return ''.join(get_item(file_path) + '\n' for _ in range(n))
        else:
            return get_item(file_path) 

    pattern = re.compile(r'(d\d+)?\[[A-Za-z ]+\]')
    print('pattern:' ,pattern)
    while True:
        new_text = pattern.sub(replace_match, text)
        if new_text == text:
            break
        text = new_text

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
        #first_line = get_first_line(filename)
        first_line = filename 
        with open(filename, 'r') as f:
            content = f.read()
        parsed_content = recursive_parse(content, first_line)
        output_filename = f"{filename}.{file_counts[filename]}"
        with open(output_filename, 'w') as f:
            f.write(parsed_content)
        print(f"Parsed {filename} -> {output_filename}")

if __name__ == '__main__':
    main()

