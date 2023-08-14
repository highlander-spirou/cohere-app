import sys
sys.path.append("..")

from sqlmodel import select, Session
from models import ChatHistory
from langchain.prompts import PromptTemplate


def get_latest_chat_history_by_section(sectionID:str, engine):
    with Session(engine) as session:
        statement = select(ChatHistory).where(ChatHistory.sectionID == sectionID).order_by(ChatHistory.id.desc()).limit(1)
        results = session.exec(statement).one_or_none()
    
    return results


def create_prompt_template(question, context=""):
    prompt_template = """Context: {context}

Question: {question}

Answer the question based on the context provided. 
"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    prompt = PROMPT.format(context=context, question=question) 
    return prompt

