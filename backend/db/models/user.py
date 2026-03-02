import uuid

from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy import UUID

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, unique=False, nullable=False)
    lastname = Column(String, unique=False, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    phone = Column(String, unique=False, nullable=False)
    department_id = Column(Integer, unique=False, nullable=True)
    designation = Column(String, unique=False, nullable=True)
    reporting_to_id = Column(Integer, unique=False, default=0)
    suspended = Column(Boolean, unique=False, default=False)
    deleted = Column(Boolean, unique=False, default=False)
    is_client = Column(Boolean, unique=False, default=False)
    created_by_id = Column(Integer, unique=False, nullable=False)
    updated_by_id = Column(Integer, unique=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_verified = Column(Boolean, unique=False, default=False) 
