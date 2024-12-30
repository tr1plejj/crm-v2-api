from beanie import Document


class Task(Document):
    user_id: int
    title: str
    description: str

    class Settings:
        name = 'tasks'

    class Config:
        extra = 'allow'
