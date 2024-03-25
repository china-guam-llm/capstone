#!/usr/bin/env python3
import pandas as pd

# Read the CSV file
df = pd.read_csv('4.0embeddings.csv')

# Filter rows based on the number of words in the "response" column
df = df[df['response'].str.split().apply(len) >= 4]

# Save the filtered data to a new CSV file
df.to_csv('4.0embeddings_filtered.csv', index=False)
