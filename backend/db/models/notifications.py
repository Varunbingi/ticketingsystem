from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.db import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    # Changed "users.id" to "user.id" to match your User model table name
    user_id = Column(Integer, ForeignKey("user.id")) 
    title = Column(String)
    message = Column(String)
    channel = Column(String) 
    read_status = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now()) 

class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    id = Column(Integer, primary_key=True)
    # Changed "users.id" to "user.id" to match your User model table name
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    inapp_enabled = Column(Boolean, default=True)