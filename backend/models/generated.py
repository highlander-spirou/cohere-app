import cohere
import pandas as pd

co = cohere.Client('Yn2c9ArMDeUtyPncAyoB2OhIJr4MtMFlOqsMGcX7')

def generate_response(text):
    response = co.generate(
        prompt=text,
        model='command-nightly'
    )
    return response

def generate_question_table(query, search_index, df):
    query_embed = co.embed(texts=[query],
                  model="embed-english-v2.0").embeddings
    
    similar_item_ids = search_index.get_nns_by_vector(query_embed[0],10,
                                                include_distances=True)
    
    question_table = pd.DataFrame(data={'texts': df.iloc[similar_item_ids[0]]['text'], 
                             'distance': similar_item_ids[1]})
    
    return question_table
#     # Choose an example (we'll retrieve others similar to it)
#     example_id = 92
#     # Retrieve nearest neighbors
#     similar_item_ids = search_index.get_nns_by_item(example_id,10,
#                                                     include_distances=True)
#     # Format and print the text and distances
#     results = pd.DataFrame(data={'texts': df.iloc[similar_item_ids[0]]['text'],
#                                 'distance': similar_item_ids[1]}).drop(example_id)
#     print(f"Question:'{df.iloc[example_id]['text']}'\nNearest neighbors:")
#     results