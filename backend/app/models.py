from sqlalchemy import Column, Integer, String, Text, DateTime
from .db import Base
from datetime import datetime

class Screenshot(Base):
    __tablename__ = "screenshots"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    filename = Column(String)
    s3_key = Column(String, unique=True)
    extracted_text = Column(Text)
    upload_time = Column(DateTime, default=datetime.utcnow)
    category = Column(String, index=True)  # New column for categorization 