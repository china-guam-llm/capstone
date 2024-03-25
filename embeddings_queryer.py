#!/usr/bin/env python3
import pandas as pd
from openai import OpenAI
import openai
import csv
from tqdm import tqdm

api_key = open("credentials/openai-key.txt", "r").read().strip("\n")
client = OpenAI(api_key=api_key)


def get_embeddings(sentences, model="text-embedding-ada-002"):
    embeddings = []
    for sentence in sentences:
        sentence = sentence.replace("\n", " ")
        response = client.embeddings.create(input=[sentence], model=model).data[0].embedding
        embeddings.append(response)
    return embeddings

df = pd.read_csv("3.5_MEGA_NUMBERED.csv")

new_rows = []

for index, row in tqdm(df.iterrows(), desc="Processing CSV Rows", total=len(df)):
    response_text = str(row["response"])
    sentences = [sentence.strip() for sentence in response_text.split(".") if sentence.strip()]
    sentence_embeddings = get_embeddings(sentences)

    for sentence, embedding in zip(sentences, sentence_embeddings):
        new_row = {
            "question": row["question"],
            "translation_variant": row["translation_variant"],
            "response": sentence,
            "embedding": embedding
        }
        new_rows.append(new_row)

new_df = pd.DataFrame(new_rows)
new_df.to_csv("embeddings.csv", index=False)
