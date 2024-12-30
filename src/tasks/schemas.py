from pydantic import BaseModel


class TaskSchema(BaseModel):
    title: str
    description: str

    class Config:
        extra = 'allow'