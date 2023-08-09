import cohere
co = cohere.Client('Yn2c9ArMDeUtyPncAyoB2OhIJr4MtMFlOqsMGcX7')

def embeding_fn(texts):
    response = co.embed(
    texts=texts,
    model='small',
    )
    return response