from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    points = Column(Integer, default=0)
    media_link = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    shifts = relationship("UserShift")
    achievements = relationship("UserAchievement")
    task_responses = relationship("TaskResponse")


class UserShift(Base):
    __tablename__ = "user_shifts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))

    user = relationship("User", back_populates="shifts")
    camp = relationship("Shift", back_populates="users")


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    participants_number = Column(Integer, nullable=False, default=0)
    start_date = Column(type_=TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(type_=TIMESTAMP(timezone=True), nullable=False)

    users = relationship("UserShift")


class ShiftReservation(Base):
    __tablename__ = "shift_reservations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(type_=TIMESTAMP(timezone=True), server_default=func.now())
    approved = Column(Boolean, default=False)

    shift = relationship("Shift")
    user = relationship("User")


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="users")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    users = relationship("UserAchievement")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    points = Column(Integer, nullable=False)
    start_date = Column(type_=TIMESTAMP(timezone=True), server_default=func.now())
    end_date = Column(type_=TIMESTAMP(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)

    responses = relationship("TaskResponse", back_populates="task")


class TaskResponse(Base):
    __tablename__ = "task_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    response_time = Column(type_=TIMESTAMP(timezone=True), server_default=func.now())
    is_approved = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    is_checked = Column(Boolean, default=False)

    user = relationship("User")
    task = relationship("Task")


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True), server_default=func.now())
