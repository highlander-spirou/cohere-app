from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional


class ChatHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    roomID: str
    contentTz: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    content: str
    answer: Optional[str]
