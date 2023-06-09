from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class TaskResponse(Base):
    __tablename__ = 'task_responses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String, ForeignKey('users.email'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    answer = Column(String, default=None)
    response_time = Column(type_=TIMESTAMP(timezone=True), server_default=func.now())
    is_approved = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    is_checked = Column(Boolean, default=False)


class ShiftReservation(Base):
    __tablename__ = 'shift_reservations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    shift_id = Column(Integer, ForeignKey('shifts.id'))
    user_email = Column(String, ForeignKey('users.email'))
    created_at = Column(type_=TIMESTAMP(timezone=True), server_default=func.now())
    is_approved = Column(Boolean, default=False)


class UserAchievement(Base):
    __tablename__ = 'user_achievements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String, ForeignKey('users.email'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    points = Column(Integer, default=0)
    media_link = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    registered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    shifts = relationship('Shift', secondary='shift_reservations', back_populates='users')
    tasks = relationship('Task', secondary='task_responses', back_populates='users')
    achievements = relationship('Achievement', secondary='user_achievements', back_populates='users')


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    number = Column(String, nullable=False)
    description = Column(String, nullable=False)
    participants_number = Column(Integer, nullable=False, default=0)
    start_date = Column(type_=TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(type_=TIMESTAMP(timezone=True), nullable=False)

    users = relationship('User', secondary='shift_reservations', back_populates='shifts')


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    author_email = Column(String, ForeignKey("users.email"))
    points = Column(Integer, nullable=False)
    start_date = Column(type_=TIMESTAMP(timezone=True), server_default=func.now())
    end_date = Column(type_=TIMESTAMP(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)

    users = relationship('User', secondary='task_responses', back_populates='tasks')


class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    users = relationship('User', secondary='user_achievements', back_populates='achievements')


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True), server_default=func.now())
