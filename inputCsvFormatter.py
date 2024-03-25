#!/usr/bin/env python3

import csv
import math

def format_text(input_file):
    # Read the contents of the input file
    with open(input_file, 'r') as file:
        text = file.read()

    # Split the text into paragraphs based on empty lines
    paragraphs = text.split('\n\n')

    # Remove any leading or trailing whitespace from each paragraph
    formatted_paragraphs = [paragraph.strip() for paragraph in paragraphs]

    return formatted_paragraphs

def write_to_csv(paragraphs, output_file):
    # Write the paragraphs to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['text'])
        writer.writerows([[paragraph] for paragraph in paragraphs])

# Example usage
input_file = 'input.txt'
formatted_paragraphs = format_text(input_file)

# Split paragraphs into 15 groups of 10 questions each
group_size = 10
num_groups = math.ceil(len(formatted_paragraphs) / group_size)

for group_index in range(num_groups):
    start_index = group_index * group_size
    end_index = start_index + group_size
    group_paragraphs = formatted_paragraphs[start_index:end_index]

    output_file = f'input_group_{group_index + 1}.csv'
    write_to_csv(group_paragraphs, output_file)
