from datetime import datetime

from sqlalchemy import DateTime, func, Text, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from schema.task import TaskStatus


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    assignee: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str] = mapped_column(Enum(TaskStatus), default=TaskStatus.TODO)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())
