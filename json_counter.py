#!/usr/bin/env python3
import json
from collections import Counter

def summarize_json(json_data):
    summary = Counter()

    for question, translations in json_data.items():
        for translation_variant, responses in translations.items():
            summary[question] += len(responses)

    return summary

if __name__ == "__main__":
    input_json_file = '3.5_MEGA.json'

    with open(input_json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    question_summary = summarize_json(json_data)

    print("Summary by question:")
    i = 0
    for question, count in question_summary.items():
        print(f"{i}\t{question[:50]}: {count} items")
        i+=1
        if i % 5 == 0:
            print("\n")
