#!/usr/bin/env python3
import json
import csv

def json_to_csv(json_data):
    rows = []

    for question, translations in json_data.items():
        for translation_variant, responses in translations.items():
            for response_number, response_text in responses.items():
                rows.append([question, translation_variant, response_text])
    return rows

def save_to_csv(rows, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['question', 'translation_variant', 'response'])
        writer.writerows(rows)

if __name__ == "__main__":
    input_json_file = '4.0_MEGA.json'
    output_csv_file = '4.0_MEGA.csv'

    with open(input_json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    csv_rows = json_to_csv(json_data)

    save_to_csv(csv_rows, output_csv_file)

    print(f'CSV file has been created: {output_csv_file}')
