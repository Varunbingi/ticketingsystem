from db.db import Base
from sqlalchemy import Column, Integer, Date, DateTime, Boolean, func


class Contract(Base):

    __tablename__ = 'client_contract'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, index=True)
    startdate = Column(Date, nullable=True)
    enddate = Column(Date, nullable=True)
    hours = Column(Integer, nullable=True, default=False)
    frequency = Column(Integer, nullable=True, default=False)
    status = Column(Boolean, nullable=True, default=False)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())    
