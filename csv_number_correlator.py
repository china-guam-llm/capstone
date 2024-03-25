#!/usr/bin/env python3
import csv

input_numbered_csv_file = 'input_numbered.csv'
mega_csv_file = '4.0_MEGA.csv'
output_csv_file = '4.0_MEGA_NUMBERED.csv'

numbered_questions = {}
with open(input_numbered_csv_file, 'r', newline='', encoding='utf-8') as input_file:
    reader = csv.reader(input_file)
    header = next(reader)  # Read the header line

    for row in reader:
        question_number, question = row[0], row[1]
        numbered_questions[question] = question_number

# Replace questions in .csv with question numbers
with open(mega_csv_file, 'r', newline='', encoding='utf-8') as mega_file:
    reader = csv.DictReader(mega_file)
    mega_data = list(reader)

    for row in mega_data:
        question = row['question']
        if question in numbered_questions:
            row['question'] = numbered_questions[question]

# write updated data to .csv
with open(output_csv_file, 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=mega_data[0].keys())
    writer.writeheader()
    writer.writerows(mega_data)

print(f'Updated CSV file with question numbers has been created: {output_csv_file}')
