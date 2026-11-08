from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ResourceModel(Base):
  __tablename__ = "resources"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  url = Column(String, unique=True, index=True, nullable=False)
  title = Column(String, nullable=True)
  summary = Column(Text, nullable=True)  # 儲存條列式摘要
  tags = Column(String, nullable=True)  # 以逗號分隔的標籤，例如 "Python,FastAPI"
  created_at = Column(DateTime, default=datetime.utcnow)
