from typing import Optional

from sqlalchemy.orm import Session

import appException

from database.task import Task
from repository.task import TaskRepository
from schema.task import TaskIn, TaskUpdate, TaskStatus

from service.service import DefaultService


class TaskService(DefaultService):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self.repo = TaskRepository(session)

    def create(self, data: TaskIn) -> Task:
        return self.repo.create(data)

    def get(self, task_id: int) -> Task:
        task = self.repo.get(task_id)
        if not task:
            raise appException.task.TaskNotFound()
        return task

    def list(self, assignee: Optional[str] = None, status: Optional[TaskStatus] = None) -> list[Task]:
        return self.repo.list(assignee=assignee, status=status)

    def update(self, task_id: int, data: TaskUpdate) -> Task:
        task = self.get(task_id)
        if task.status == TaskStatus.DONE and data.status and data.status != TaskStatus.DONE:
            raise appException.task.TaskStatusRollbackForbidden(task.status, data.status)
        return self.repo.update(task, data)

    def delete(self, task_id: int) -> None:
        task = self.get(task_id)
        self.repo.delete(task)