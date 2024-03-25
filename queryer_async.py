#!/usr/bin/env python3
import openai
import json
import csv
import asyncio
import aiohttp
from   google.cloud import translate_v2 as Translate

# number of times to repeat each query. 10 * 3 = 30 response per question
QUERY_REPETITIONS = 10
ASYNC_TIMEOUT = 1000

MAX_RETRIES = 3  # Maximum number of retries for each operation

# OpenAI API key
openai.api_key = open("credentials/openai-key.txt", "r").read().strip("\n")

# Google Cloud API key
api_key_path = "credentials/translate-key.json"
translate_client = Translate.Client.from_service_account_json(api_key_path)

# Translates text into the target language, must be valid ISO 639-1 language code
def translate(target: str, text: str) -> dict:
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]

# Using 3 variants
def translate_to_chinese_variants(text):
    chinese_variants = {
        'zh':    translate('zh', text),         #Chinese simplfied
        'zh-CN': translate('zh-CN', text),      #Chinese simplified, People's Republic of China
        'zh-TW': translate('zh-TW', text)       #Taiwanese Mandarin
    }
    return chinese_variants

async def translate_to_english(response, retry_count=0):
    try:
        if isinstance(response, bytes):
            response = response.decode("utf-8")

        result = translate_client.translate(response, target_language='en')
        return result["translatedText"]
    except Exception as e:
        print(f"Translation error: {e}")

        if retry_count < MAX_RETRIES:
            print(f"Retrying translation... Attempt {retry_count + 1}")
            await asyncio.sleep(5)  # Introduce a delay before retrying
            return await translate_to_english(response, retry_count + 1)
        else:
            print(f"Max retries reached. Skipping this translation.")
            return None

async def chatgpt_async_call(translation: str, retry_count=0):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=ASYNC_TIMEOUT)) as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai.api_key}"},
                json={
                    "model": "gpt-4-turbo-preview",
                    "messages": [{"role": "user", "content": f"{translation}"}],
                },
            ) as response:
                data = await response.json()
                return data["choices"][0]["message"]["content"]
    except KeyError as e:
        # If the 'choices' key is not present in the response
        print(f"KeyError: {e}")

        if retry_count < MAX_RETRIES:
            print(f"Retrying ChatGPT call... Attempt {retry_count + 1}")
            await asyncio.sleep(5)  # Introduce a delay before retrying
            return await chatgpt_async_call(translation, retry_count + 1)
        else:
            print(f"Max retries reached. Skipping this ChatGPT call.")
            return None
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"An error occurred: {e}")

        if retry_count < MAX_RETRIES:
            print(f"Retrying... Attempt {retry_count + 1}")
            await asyncio.sleep(5)  # delay before retrying
            return await chatgpt_async_call(translation, retry_count + 1)
        else:
            print(f"Max retries reached. Skipping this ChatGPT call.")
            return None

def process_csv(input_file):
    translations_dict = {}

    with open(input_file, 'r', encoding='utf-8') as csv_input:
        reader = csv.DictReader(csv_input)

        for row in reader:
            # csv column starts with 'text'
            english_prompt = row.get('text', '')

            if english_prompt:
                translations_dict[english_prompt] = translate_to_chinese_variants(english_prompt)

    return translations_dict

# async def chatgpt_processing(translations: dict, num_iterations: int = QUERY_REPETITIONS):
#     responses_dict = {}

#     for english_prompt, chinese_variants in translations.items():
#         response_variants = {}

#         for variant, translation in chinese_variants.items():
#             print(f"Making {num_iterations} ChatGPT calls for {variant}:\t{translation}")
#             # ASYNCHRONOUS CALLS TO CHATGPT FOR EACH VARIANT
#             tasks = [chatgpt_async_call(translation) for _ in range(num_iterations)]
#             responses = await asyncio.gather(*tasks)
#             response_dict = {index + 1: response for index, response in enumerate(responses)}
#             response_variants[variant] = response_dict

#         responses_dict[english_prompt] = response_variants

#     return responses_dict

async def chatgpt_processing(translations: dict, num_iterations: int = QUERY_REPETITIONS):
    responses_dict = {}

    for english_prompt, chinese_variants in translations.items():
        response_variants = {}

        for variant, translation in chinese_variants.items():
            print(f"Making {num_iterations} ChatGPT calls for {variant}:\t{translation}")
            # ASYNCHRONOUS CALLS TO CHATGPT FOR EACH VARIANT
            tasks = [chatgpt_async_call(translation) for _ in range(num_iterations)]
            responses = await asyncio.gather(*tasks)
            response_dict = {index + 1: response for index, response in enumerate(responses)}
            response_variants[variant] = response_dict

            # Introduce a delay between iterations
            await asyncio.sleep(2)  # Adjust the sleep duration as needed

        responses_dict[english_prompt] = response_variants

    return responses_dict

async def translate_respones_to_english(translations_with_responses):
    translated_responses = {}

    for english_prompt, response_variants in translations_with_responses.items():
        translated_variants = {}

        for variant, response_dict in response_variants.items():
            translated_responses_dict = {}
            tasks = [translate_to_english(response) for response in response_dict.values()]
            translated_responses_list = await asyncio.gather(*tasks)

            for index, translation in enumerate(translated_responses_list):
                translated_responses_dict[index + 1] = translation

            translated_variants[variant] = translated_responses_dict

        translated_responses[english_prompt] = translated_variants

    return translated_responses

def print_translations(translations: dict):
    print("\nTRANSLATIONS")
    for english_prompt, chinese_variants in translations.items():
        print(f"English: {english_prompt}")
        for variant, translation in chinese_variants.items():
            print(f"{variant}:\t{translation}")
        print("=" * 50)

def print_responses(translations_with_responses: dict):
    print("\nRESPONSES:")
    for english_prompt, response_variants in translations_with_responses.items():
        print(f"English: {english_prompt}")
        for variant, response_dict in response_variants.items():
            print(f"{variant}:")
            for index, response in response_dict.items():
                print(f"  {index}: {response}")
            print()  # Add newline between variants
        print("=" * 50)

def print_translated_responses(translated_responses: dict):
    print("\nTRANSLATED RESPONSES")
    for english_prompt, translated_variants in translated_responses.items():
        print(f"English: {english_prompt}")
        for variant, translation_dict in translated_variants.items():
            print(f"{variant}:")
            for index, translation in translation_dict.items():
                translation_str = str(translation)
                print(f"  {index}:\t{translation_str}")
            print()  # Add a newline between variants
        print("=" * 50)

# can use this if you want to make a csv instead of json
def write_csv(translated_responses: dict):
    with open('translated_responses.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Question in English', 'zh_response in English', 'zh_CN response in English', 'zh_TW response in English'])
        for english_prompt, translated_variants in translated_responses.items():
            row = [english_prompt]
            for variant, translation in translated_variants.items():
                row.append(translation)
            csv_writer.writerow(row)

def write_json(translated_responses: dict):
    with open('4.0translated_responses_group13.json', 'w', encoding='utf-8') as json_file:
        json.dump(translated_responses, json_file, ensure_ascii=False, indent=4)

def clean_up_json(json_data):
    cleaned_json = json_data.copy()

    for english_prompt, translations in json_data.items():
        for variant, responses in translations.items():
            for index, response in responses.items():
                # fix encoding issue
                cleaned_response = response.replace('&#39;', "'")           # '
                cleaned_response = cleaned_response.replace('&quot;', '"')  # "
                cleaned_response = cleaned_response.replace('&amp;', '&')   # &
                cleaned_json[english_prompt][variant][index] = cleaned_response

    return cleaned_json

# function to print all currently supported language codes
def list_languages() -> dict:
    """Lists all available languages."""
    results = translate_client.get_languages()
    for language in results:
        print("{name} ({language})".format(**language))
    return results

async def main_async():
    try:
        translations = process_csv('input_group_13.csv')
        print_translations(translations)

        translations_with_responses = await chatgpt_processing(translations)
        print_responses(translations_with_responses)

        translated_responses = await translate_respones_to_english(translations_with_responses)
        cleaned_translated_responses = clean_up_json(translated_responses)
        print_translated_responses(cleaned_translated_responses)

        write_json(cleaned_translated_responses)

        # write_csv(translated_responses)   # optional, writes to csv
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main_async())
