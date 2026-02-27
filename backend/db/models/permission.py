from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class PermissionCategory(Base):
    __tablename__ = 'permission_category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    shortname = Column(String, unique=True)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Permission(Base):
    
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    permission_category_id = Column(Integer, index=True)
    name = Column(String)
    shortname = Column(String, unique=True)
    description = Column(String, nullable=True)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class UserPermission(Base):
    
    __tablename__ = 'user_permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    permission_category_id = Column(Integer, index=True)
    permission_id = Column(Integer, index=True)
    userid = Column(Integer, index=True)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())