import os
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import (Column, String, UUID, ForeignKey, BigInteger, ARRAY, Integer)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

#load_dotenv()

db_url = ""

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


if __name__ == '__main__':
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
