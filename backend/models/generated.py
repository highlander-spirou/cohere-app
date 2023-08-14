import cohere
import pandas as pd

from datasets import load_dataset
from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate, ChatPromptTemplate
# from langchain.chains import RetrievalQA
from langchain.llms import Cohere
from os.path import exists

co = cohere.Client('Yn2c9ArMDeUtyPncAyoB2OhIJr4MtMFlOqsMGcX7')

prompt_template = """Context: {context}

Question: {question}

Answer the question based on the context provided. 
"""


def generate_response(text):
    response = co.generate(
        prompt=text,
        model='command-light-nightly',
        temperature=1,
        max_tokens=500,
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

def get_cohere_response(response):
    return response.generations[0][0].text


def langchain_test():
    # embeddings = CohereEmbeddings(cohere_api_key='Yn2c9ArMDeUtyPncAyoB2OhIJr4MtMFlOqsMGcX7')
    # if exists('./chroma_db') is False:
    #     print('DB not found')
    #     dataset = load_dataset("trec", split="train")
    #     df = pd.DataFrame(dataset)[:10]
    #     text_list = [Document(page_content=i) for i in df['text'].values]
    #     vectordb = Chroma.from_documents(text_list, embedding=embeddings, persist_directory="./chroma_db")
    #     vectordb.persist()
    # else: 
    #     vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    questions = ["How many colours in a rainbow", 
                 "List the first 3 colour", 
                 "What is the next three", 
                 "The last color is ?"]

    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    prompt_1 = PROMPT.format(context="", question=questions[0]) 
    model = Cohere(model='command-light-nightly', temperature=1, cohere_api_key='Yn2c9ArMDeUtyPncAyoB2OhIJr4MtMFlOqsMGcX7')
    answer1 = model.generate([prompt_1])
    prev_answer = get_cohere_response(answer1)
    prompt_2 = PROMPT.format(context=prev_answer, question=questions[2]) 
    answer2 = model.generate([prompt_2])
    print(get_cohere_response(answer2))
    
    # answer2 = model.generate(PROMPT.format(context=questions[2], question=questions[3]))
    
    # print(answer2)


    # qa = ChatVectorDBChain.from_chain_type(llm=Cohere(model='command-light-nightly', temperature=1, cohere_api_key='Yn2c9ArMDeUtyPncAyoB2OhIJr4MtMFlOqsMGcX7'), 
    #                              retriever=vectordb.as_retriever(), 
    #                              chain_type_kwargs={"prompt": PROMPT})
    


    # for question in questions:
    #     answer = qa({"query": question})
    #     result = answer["result"].replace("\n","").replace("Answer:","")
    #     print("-"*150,"\n")
    #     print(f"Question: {question}")
    #     print(f"Answer: {result}")

    return 'aaa'
