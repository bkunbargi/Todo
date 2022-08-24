from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from database import Base

class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    todo = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class TodoComment(Base):
    __tablename__ = "todocomment"
    id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey('todo.id'))
    comment = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)