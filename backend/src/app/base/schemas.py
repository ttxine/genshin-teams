from pydantic import BaseModel


class Message(BaseModel):
    msg: str


class ExceptionMessage(BaseModel):
    detail: str
