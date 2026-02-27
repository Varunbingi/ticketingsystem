from db.db import Base
from sqlalchemy  import Column,Integer,String
from sqlalchemy.dialects.postgresql import ARRAY 
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

class Ticket(Base):
    __tablename__='ticket'

    id= Column(Integer, primary_key=True, index=True)
    client_id= Column(Integer, nullable=False)
    priority= Column(Integer, nullable=False)
    subject=Column(String(255), nullable=False)
    description=Column(String(1000))
    status=Column(Integer, nullable=False, default=0)
    files=Column(ARRAY(String(255)))
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  