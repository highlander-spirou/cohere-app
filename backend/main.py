from fastapi import FastAPI
from pydantic import BaseModel
from os.path import exists

from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, select, asc

from models import ChatHistory
# from helpers import get_latest_chat_history_by_section, create_prompt_template
import cohere


# Singleton variable
app = FastAPI()
engine = create_engine("sqlite:///database.sqlite3")
co = cohere.Client('Yn2c9ArMDeUtyPncAyoB2OhIJr4MtMFlOqsMGcX7')

# if exists('database.sqlite3') is False:
#     print('database not found, create a new one')
#     SQLModel.metadata.create_all(engine)
SQLModel.metadata.create_all(engine)


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

class ChatRequest(BaseModel):
    roomID: str
    content: str



@app.get("/")
async def main():
    return {"message": "Hello World"}


def create_new_chat(req:ChatRequest):
    new_chat = ChatHistory(**req.dict())
    with Session(engine) as session:
        session.add(new_chat)
        session.commit()
        session.refresh(new_chat)
    return new_chat

def update_answer_field(id, answer):
    with Session(engine) as session:
        statement = select(ChatHistory).where(ChatHistory.id == id)
        chat = session.exec(statement).one()
        chat.answer = answer
        session.add(chat)
        session.commit()
        session.refresh(chat)
    return chat


def get_room_chat_history(roomID):
    with Session(engine) as session:
        statement = select(ChatHistory).where(ChatHistory.roomID == roomID).order_by(ChatHistory.contentTz)
        chat = session.exec(statement).all()
    return chat

@app.post('/api/create-chat')
async def create_chat(req:ChatRequest):
    new_chat = create_new_chat(req)
    chat_response = update_answer_field(new_chat.id, f"Server is responding to question: {new_chat.content}")
    return {"response": chat_response.answer}

@app.get('/api/chat-history')
async def chat_history(roomID: str):
    chat_log = get_room_chat_history(roomID)
    returned_json = []
    for i in chat_log:
        returned_json.append({"userQuery": i.content, "botResponse": i.answer})
    return {"res": returned_json}


# @app.post('/chat')
# async def chat(req:ChatRequest):
#     latest_chat = get_latest_chat_history_by_section(req.sectionID, engine)
#     new_chat = create_new_chat(req)
#     if latest_chat is None:
#         context = ""
#     else:
#         context = latest_chat.content
#     prompt = create_prompt_template(req.content, context)
#     result = co.generate(prompt, model='command-light', temperature=0, max_tokens=500)
#     update_prompt_field(new_chat.id, new_prompt=result[0].text)
#     print(result[0].text)
#     return {"res": result[0].text}



# @app.post("/")
# async def embed(content: PromptRequest):
#     a = embeding_fn([content.content])
#     return  {"b": a}

# @app.post("/answer")
# async def answer(content: PromptRequest):
#     a = generate_response(content.content)
#     return  {"res": a.data}


# @app.post("/query")
# async def query(content: PromptRequest):
#     a = generate_question_table(content.content, search_index, df)
#     print(a)
#     return  {"res": a}

# @app.post("/langchain")
# async def test(content: PromptRequest):
#     a = langchain_test()
#     return  {"res": a}


