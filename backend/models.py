from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True)
    owner = Column(String(128), index=True)
    key = Column(String(256), index=True)
    value = Column(Text)
    importance = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
