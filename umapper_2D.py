#!/usr/bin/env python3
import pandas as pd
import numpy as np
import umap
import plotly.graph_objects as go
from tqdm import tqdm  # progress bar

df = pd.read_csv('4.0embeddings_filtered.csv')

# extract embedings
embeddings = df['embedding'].apply(eval).tolist()

#EDIT THESE VALUES TO CHANGE GROUPING
umap_2d = umap.UMAP(n_components=2, n_neighbors=100, min_dist=0.001)  # Set n_components to 2 for 2D visualization
embeddings_2d = umap_2d.fit_transform(embeddings)

embeddings_2d = np.array(embeddings_2d)

ids = df['question'].tolist()

grouped_ids = [list(range(i, i+5)) for i in range(1, 126, 5)]

colors = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, 25, endpoint=False)]

hover_text = [f'Question ID: {id_}<br>Sentence: {response}' for id_, response in zip(ids, df['response'])]

fig = go.Figure()
for group, color in zip(grouped_ids, colors):
    indices = [i for i, x in enumerate(ids) if x in group]
    embeddings_group = embeddings_2d[indices]
    hover_group = [hover_text[i] for i in indices]
    fig.add_trace(go.Scatter(
        x=embeddings_group[:, 0],
        y=embeddings_group[:, 1],
        mode='markers',
        marker=dict(
            size=5,
            color=color,
            opacity=0.7,
        ),
        name=f'IDs {group[0]}-{group[-1]}',
        hovertext=hover_group,  # Assign hover text (tooltips)
        hoverinfo='text'  # Show hover text on hover
    ))

fig.update_layout(
    title='2D UMAP Visualization with Hover Information',
    xaxis_title='UMAP Component 1',
    yaxis_title='UMAP Component 2',
    legend=dict(
        title='Question IDs',
    )
)

fig.write_html('4.0_umap_interactive_2d_with_hover_test.html')
