from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from .models import Task
from src.auth.config import current_active_user
from src.auth import User
from .schemas import TaskSchema

router = APIRouter(
    tags=['tasks'],
    prefix='/tasks'
)


@router.post('/new')
async def create_task(task: TaskSchema, user: User = Depends(current_active_user)):
    new_task = Task(**task.model_dump(), user_id=user.id)
    await Task.create(new_task)
    return {'message': 'created successfully'}


@router.get('/{id}')
async def get_task(id: PydanticObjectId, user: User = Depends(current_active_user)):
    task = await Task.get(document_id=id)
    return task


@router.get('/')
async def list_tasks(user: User = Depends(current_active_user)):
    tasks = await Task.find({'user_id': user.id}).to_list()
    return tasks