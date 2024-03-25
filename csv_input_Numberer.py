#!/usr/bin/env python3
import csv

input_csv_file = 'input.csv'
output_csv_file = 'input_numbered.csv'

with open(input_csv_file, 'r', newline='', encoding='utf-8') as input_file:
    reader = csv.reader(input_file, delimiter='"')
    next(reader)  # Skip  header

    data = []
    current_question_number = 0

    for row in reader:
        if row[0].strip():
            current_question_number += 1
            data.append([current_question_number, row[0]])

with open(output_csv_file, 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Question Number', 'text'])

    for row in data:
        writer.writerow(row)

print(f'CSV file with numbered questions has been created: {output_csv_file}')
