from sqlalchemy import Column, Integer, String, Date, DateTime, func
from db.db import Base

class Client(Base):

    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idnumber = Column(Integer)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
    startdate = Column(Date, nullable=False)
    enddate = Column(Date, nullable=False)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())    

class Client_users(Base):

    __tablename__ = 'client_users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    Client_users = Column(Integer, index=True)
