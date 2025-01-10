import os
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import (Column, String, UUID, ForeignKey, BigInteger, ARRAY, Integer, Time)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

#load_dotenv()

db_url = "postgresql://postgres:postgres@localhost:5432/fitbase"

engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=300)

SessionMaker = sessionmaker(bind=engine)

Base = declarative_base()


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(UUID, primary_key=True, default=uuid4)
    username = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    password = Column(String, nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True, default=uuid4)
    username = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    telegram_id = Column(BigInteger, nullable=False)


class Standards(Base):
    __tablename__ = 'standards'
    id = Column(UUID, primary_key=True, default=uuid4)
    telegram_id = Column(BigInteger, nullable=True)
    grom = Column(String, nullable=True, default='00:00')
    turkish_barbell_lifting = Column(Integer, nullable=True, default=0)
    jump_rope = Column(Integer, nullable=True, default=0)
    bench_press = Column(Integer, nullable=True, default=0)
    rod_length = Column(Integer, nullable=True, default=0)
    shuttle_run = Column(Integer, nullable=True, default=0)
    glute_bridge = Column(Integer, nullable=True, default=0)
    pull_ups = Column(Integer, nullable=True, default=0)
    cubic_jumps = Column(Integer, nullable=True, default=0)
    lifting_the_barbell_on_the_chest = Column(Integer, nullable=True, default=0)
    axel_deadlift = Column(Integer, nullable=True, default=0)
    handstand = Column(String, nullable=True, default='00:00')
    classic_squat = Column(Integer, nullable=True, default=0)
    turkish_kettlebell_lifting = Column(Integer, nullable=True, default=0)
    push_ups = Column(Integer, nullable=True, default=0)
    lifting_barbell_on_the_chest = Column(Integer, nullable=True, default=0)
    walking_kettlebells = Column(Integer, nullable=True, default=0)
    deadlift = Column(Integer, nullable=True, default=0)
    long_jump = Column(Integer, nullable=True, default=0)
    barbell_jerk = Column(Integer, nullable=True, default=0)
    axel_hold = Column(String, nullable=True, default='00:00')
    front_squat = Column(Integer, nullable=True, default=0)


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
