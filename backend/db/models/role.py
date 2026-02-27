from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class Role(Base):

    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    shortname = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class RoleUser(Base):

    __tablename__ = 'user_role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, index=True)
    roleid = Column(Integer, index=True)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())    