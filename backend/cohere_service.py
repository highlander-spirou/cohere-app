# This is a standalone service, run this to create embeded vector on the fly 
# This software is independ from the main.py which is the server
# After running cohere_service, embeded text will be saved on the models/data
# Then the route `answer` can be run

from datasets import load_dataset
import pandas as pd
import cohere
from annoy import AnnoyIndex
import numpy as np
from os.path import exists

co = cohere.Client('Yn2c9ArMDeUtyPncAyoB2OhIJr4MtMFlOqsMGcX7')
embeds_initial_shape = 4096

if exists('seeded_embeds.ann'):
    print('file existed')
    search_index = AnnoyIndex(embeds_initial_shape, 'angular')
    search_index.load('seeded_embeds.ann')
    df = pd.read_csv('df.csv')

else:
    print('file not existed')
    # Get dataset
    dataset = load_dataset("trec", split="train")
    df = pd.DataFrame(dataset)[:1000]
    df.to_csv('df.csv')

    embeds = co.embed(texts=list(df['text']),
                    model='embed-english-v2.0').embeddings


    search_index = AnnoyIndex(np.array(embeds).shape[1], 'angular')

    for i in range(len(embeds)):
        search_index.add_item(i, embeds[i])

    search_index.build(10) # 10 trees
    search_index.save('seeded_embeds.ann')

    

# query = "What is the tallest mountain in the world?"
# query_embed = co.embed(texts=[query],
#                   model="embed-english-v2.0").embeddings

# similar_item_ids = search_index.get_nns_by_vector(query_embed[0],10,
#                                                 include_distances=True)

# results = pd.DataFrame(data={'texts': df.iloc[similar_item_ids[0]]['text'], 
#                              'distance': similar_item_ids[1]})

# print(f"Query:'{query}'\nNearest neighbors:")
# print('results', results)
