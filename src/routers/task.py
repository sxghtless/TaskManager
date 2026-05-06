from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_session
from schema.task import TaskIn, TaskOut, TaskUpdate, TaskStatus
from service.task import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut, status_code=201)
def create_task(data: TaskIn, db: Session = Depends(get_session)):
    return TaskService(db).create(data)


@router.get("/", response_model=list[TaskOut], responses={
    404: {"description": "Task not found",
          "content": {"application/json": {"example": {"status_code": 404, "message": "task not found"}}}},
})
def list_tasks(assignee: Optional[str] = None, status: Optional[TaskStatus] = None, db: Session = Depends(get_session)):
    return TaskService(db).list(assignee=assignee, status=status)


@router.get("/{task_id}", response_model=TaskOut, responses={
    404: {"description": "Task not found",
          "content": {"application/json": {"example": {"status_code": 404, "message": "task not found"}}}},
})
def get_task(task_id: int, db: Session = Depends(get_session)):
    return TaskService(db).get(task_id)


@router.patch("/{task_id}", response_model=TaskOut, responses={
    400: {"description": "Status rollback forbidden",
          "content": {"application/json": {"example": {"status_code": 400, "message": "Jumping back from 'DONE' is not possible"}}}},
    404: {"description": "Task not found",
          "content": {"application/json": {"example": {"status_code": 404, "message": "task not found"}}}},
})
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_session)):
    return TaskService(db).update(task_id, data)


@router.delete("/{task_id}", status_code=204, responses={
    404: {"description": "Task not found", "content": {"application/json": {"example": {"status_code": 404, "message": "task not found"}}}},
})
def delete_task(task_id: int, db: Session = Depends(get_session)):
    TaskService(db).delete(task_id)