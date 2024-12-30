from beanie import Document


class Task(Document):
    user_id: int
    title: str
    description: str
    additional_data: dict | None = None

    class Settings:
        name = 'tasks'

    class Config:
        schema_extra = 'allow'
