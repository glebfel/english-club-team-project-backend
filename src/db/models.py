from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    camps = relationship("UserCamp", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    task_responses = relationship("TaskResponse", back_populates="user")


class UserShifts(Base):
    __tablename__ = "user_shifts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    camp_id = Column(Integer, ForeignKey("shifts.id"))

    user = relationship("User", back_populates="shifts")
    camp = relationship("Shift", back_populates="users")


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    users = relationship("UserShifts", back_populates="user_shifts")


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

    users = relationship("UserAchievement", back_populates="user_achievements")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Boolean, default=False)

    responses = relationship("TaskResponse", back_populates="task")


class TaskResponse(Base):
    __tablename__ = "task_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    response = Column(String, nullable=False)
    response_time = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="users")
    task = relationship("Task", back_populates="responses")


class ShiftReservation(Base):
    __tablename__ = "shift_reservations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    approved = Column(Boolean, default=False)

    shift = relationship("Shift")
    user = relationship("User")


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
