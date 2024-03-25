#!/usr/bin/env python3
import json
import os

def combine_json_files(output_file):
    combined_data = {}

    file_names = [
        "GPT4.0_json_results/4.0translated_responses_group1.json",
        "GPT4.0_json_results/4.0translated_responses_group2.json",
        "GPT4.0_json_results/4.0translated_responses_group3.json",
        "GPT4.0_json_results/4.0translated_responses_group4.json",
        "GPT4.0_json_results/4.0translated_responses_group5.json",
        "GPT4.0_json_results/4.0translated_responses_group6.json",
        "GPT4.0_json_results/4.0translated_responses_group7.json",
        "GPT4.0_json_results/4.0translated_responses_group8.json",
        "GPT4.0_json_results/4.0translated_responses_group9.json",
        "GPT4.0_json_results/4.0translated_responses_group10.json",
        "GPT4.0_json_results/4.0translated_responses_group11.json",
        "GPT4.0_json_results/4.0translated_responses_group12.json",
        "GPT4.0_json_results/4.0translated_responses_group13.json",
    ]

    current_directory = os.getcwd()

    for filename in file_names:
        file_path = os.path.join(current_directory, filename)

        # Load JSON content from the current file
        with open(file_path, 'r') as file:
            data = json.load(file)

        combined_data.update(data)

    with open(output_file, 'w') as output_file:
        json.dump(combined_data, output_file, indent=2)

output_file = "4.0_MEGA.json"
combine_json_files(output_file)
