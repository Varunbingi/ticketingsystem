from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base
from datetime import datetime


class AppLog(Base):
    __tablename__ = "app_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, default="-")
    filename = Column(String, default="-")
    lineno = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)  # FK to users.id

    path = Column(String, default="-")
    method = Column(String, default="-")
    request_id = Column(String, default="-")
    trace_id = Column(String, default="-")
    span_id = Column(String, default="-")
    span_name = Column(String, default="-")
    duration_ms = Column(Float, default=0.0)

    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to User table
    user = relationship("User", backref="logs")