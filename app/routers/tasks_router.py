"""
This module defines the FastAPI router for the tasks API. It includes the following routes:

- `POST /`: Create a new task.
- `GET /{task_id}`: Retrieve a task by its ID.
- `GET /`: Retrieve a list of all tasks.
- `PUT /{task_id}`: Update an existing task by its ID.
- `DELETE /all`: Delete all tasks.
- `DELETE /{task_id}`: Delete a task by its ID.
"""
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from models import Task, UpdateTaskModel, TaskList
from db import db

"""
The FastAPI router for the tasks API. This router defines the routes for managing tasks, including creating, retrieving, updating, and deleting tasks.
"""
tasks_router = APIRouter()


@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    try:
        # Additional validation for task data
        if not task.title or len(task.title) > 100:
            raise ValueError("Task title is required and must not exceed 100 characters")
        if task.description and len(task.description) > 500:
            raise ValueError("Task description must not exceed 500 characters")

        return db.add_task(task)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)


@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@tasks_router.delete("/all", response_model=dict)
async def delete_all_tasks():
    db.delete_all_tasks()
    return {"message": "All tasks have been deleted"}


@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}
