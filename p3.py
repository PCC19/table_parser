import random
import sys
import re
import os

def replace_dicerolls(text):
    # Pattern to match diceroll strings like '3d6+2', '1d20-1', '2d10', etc.
    pattern = r'(\d+)d(\d+)([+-]\d+)?'

    def roll_dice(match):
        num_dice = int(match.group(1))
        dice_sides = int(match.group(2))
        modifier = match.group(3)
        modifier_value = int(modifier) if modifier else 0

        # Roll the dice num_dice times and sum the results
        total = sum(random.randint(1, dice_sides) for _ in range(num_dice))
        # Add the modifier
        total += modifier_value
        return str(total)

    # Substitute all diceroll patterns in the text with their calculated values
    result_text = re.sub(pattern, roll_dice, text)
    return result_text

def get_item(input_str, delimiter):
    if os.path.isfile(input_str):
        with open(input_str, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
            if lines:
                data = [line.split(delimiter) for line in lines]
        
                # Check if the file has only one column
                if all(len(row) == 1 for row in data):
                    # Return a random line as string
                    return random.choice(data)[0]
        
                # Check if all first column entries are numbers
                first_col = [row[0] for row in data if len(row) > 1]
                if all(item.isdigit() for item in first_col):
                    # Pick a random row and return the second column
                    row = random.choice([row for row in data if len(row) > 1])
                    return row[1]
                
                # Check for interval format (e.g., "3-6")
                intervals = []
                for row in data:
                    if len(row) > 1 and '-' in row[0]:
                        parts = row[0].split('-')
                        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                            intervals.append((int(parts[0]), int(parts[1]), row[1]))
                if intervals:
                    # Find the min and max across all intervals
                    min_val = min(start for start, end, _ in intervals)
                    max_val = max(end for start, end, _ in intervals)
                    rand_num = random.randint(min_val, max_val)
                    for start, end, value in intervals:
                        if start <= rand_num <= end:
                            return value
                
                # If none of the above, return empty string
                return ''
            else:
                return ""  # Returns empty string if the file is empty
    else:
        return input_str

def process_string(input_string):
    def replacer(match):
        number_text = match.group(1).strip()
        parts = number_text.split(maxsplit=1)
        if len(parts) == 1:
            # Only text, no number
            number = 1
            text = parts[0]
        else:
            try:
                number = int(parts[0])
                if number == 0:
                    number = 1
                text = parts[1]
            except ValueError:
                # If first part is not a number, treat whole as text
                number = 1
                text = number_text
        results = [get_item(text,',') for _ in range(number)]
        return '\n'.join(results)
    return re.sub(r'\[(.*?)\]', replacer, input_string)

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
            text = f.read()
        #parsed_content = recursive_parse(content, first_line)
        i = 0
        print("text a: ",i, text)
        while True:
            new_text = replace_dicerolls(text)
            print("text b: ",i, new_text)
            new_text = process_string(new_text)
            print("text c: ",i, new_text)
            if new_text == text:
                break
            text = new_text
            i = i + 1
        #parsed_content = replace_dicefolls(content)
        #print("1: ", parsed_content)
        #parsed_content = process_string(parsed_content)
        #print("2: ", parsed_content)
        output_filename = f"{filename}.{file_counts[filename]}"
        with open(output_filename, 'w') as f:
            f.write(text)
        print(f"Parsed {filename} -> {output_filename}")

if __name__ == '__main__':
    main()

