from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Path
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
    return new_task


@router.get('/{document_id}')
async def get_task(document_id: Annotated[PydanticObjectId, Path()], user: User = Depends(current_active_user)):
    task = await Task.get(document_id=document_id)
    return task


@router.get('/')
async def list_tasks(user: User = Depends(current_active_user)):
    tasks = await Task.find({'user_id': user.id}).to_list()
    return tasks