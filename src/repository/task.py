from typing import Optional

from sqlalchemy.orm import Session

from database.task import Task
from schema.task import TaskIn, TaskUpdate, TaskStatus


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: TaskIn) -> Task:
        task = Task(**data.model_dump())
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get(self, task_id: int) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def list(self, assignee: Optional[str] = None, status: Optional[TaskStatus] = None) -> list[Task]:
        task = self.session.query(Task)
        if assignee:
            task = task.filter(Task.assignee == assignee)
        if status:
            task = task.filter(Task.status == status)
        return task.all()

    def update(self, task: Task, data: TaskUpdate) -> Task:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(task, field, value)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()