from fastapi import FastAPI
from pydantic import BaseModel
from models.embeded import embeding_fn
from models.generated import generate_response, generate_question_table
from cohere_service import df, search_index

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}


class PromptRequest(BaseModel):
    content: str

@app.post("/")
async def embed(content: PromptRequest):
    a = embeding_fn([content.content])
    return  {"b": a}

@app.post("/answer")
async def answer(content: PromptRequest):
    a = generate_response(content.content)
    return  {"res": a.data}


@app.post("/query")
async def query(content: PromptRequest):
    a = generate_question_table(content.content, search_index, df)
    print(a)
    return  {"res": a}


