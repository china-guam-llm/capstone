#!/usr/bin/env python3
import asyncio
import pandas as pd
from openai import OpenAI
from tqdm.asyncio import tqdm as async_tqdm

api_key = open("credentials/openai-key.txt", "r").read().strip("\n")
client = OpenAI(api_key=api_key)

async def get_embedding(sentence, model="text-embedding-ada-002"):
    sentence = sentence.replace("\n", " ")
    response = await asyncio.to_thread(client.embeddings.create, input=[sentence], model=model)
    embedding = response.data[0].embedding
    return embedding

def split_sentences(text):
    sentences = text.split('.')
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

async def process_rows(row):
    response_text = str(row["response"])
    sentences = split_sentences(response_text)
    tasks = [get_embedding(sentence) for sentence in sentences]
    embeddings = await asyncio.gather(*tasks)
    new_rows = []
    for sentence, embedding in zip(sentences, embeddings):
        new_row = {
            "question": row["question"],
            "translation_variant": row["translation_variant"],
            "response": sentence,
            "embedding": embedding
        }
        new_rows.append(new_row)

    return new_rows

async def main():
    df = pd.read_csv("4.0_MEGA_NUMBERED2.csv")

    new_rows = []
    tasks = []

    for index, row in df.iterrows():
        tasks.append(process_rows(row))

    for task in async_tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Processing Rows"):
        new_rows.extend(await task)

    new_df = pd.DataFrame(new_rows)
    new_df.to_csv("4.0embeddings.csv", index=False)

if __name__ == "__main__":
    asyncio.run(main())
