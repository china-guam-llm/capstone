#!/usr/bin/env python3
import csv
from collections import Counter

def count_responses_per_question(csv_file_path):
    questions_counter = Counter()

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            question_number = row['question'][:150]
            questions_counter[question_number] += 1

    return questions_counter

if __name__ == "__main__":
    input_csv_file = '3.5_MEGA.csv'

    response_counts = count_responses_per_question(input_csv_file)

    print("Breakdown of responses per question:")
    i=1
    for question_number, count in response_counts.items():
        if count == 30:
            print(f"Question {i}{question_number}: {count} responses")
        else:
            print(f"Question {i}{question_number}: {count} responses, that's fucked up")
        i+=1
