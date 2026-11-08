from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. 資料庫連線設定 (使用 SQLite)
DATABASE_URL = "sqlite:///./vault.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 2. SQLAlchemy Model
class ResourceModel(Base):
  __tablename__ = "resources"
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  url = Column(String, unique=True, index=True, nullable=False)
  title = Column(String, nullable=True)
  summary = Column(Text, nullable=True)
  tags = Column(String, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)

# 3. Pydantic Schemas
class LinkCreate(BaseModel):
  url: HttpUrl


class ResourceResponse(BaseModel):
  id: int
  url: str
  title: str
  summary: str
  tags: str
  created_at: datetime

  class Config:
    from_attributes = True


# 4. FastAPI 應用程式初始化
app = FastAPI(title="Link Summarizer API", version="1.0.0")


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


# 5. 核心 API 端點：接收網址並處理
@app.post("/api/resources", response_model=ResourceResponse)
def create_resource(payload: LinkCreate, db=Depends(get_db)):
  url_str = str(payload.url)

  # 檢查是否已存在
  existing = (
      db.query(ResourceModel).filter(ResourceModel.url == url_str).first()
  )
  if existing:
    raise HTTPException(status_code=400, detail="此鏈結已經存在於 Vault 中")

  # 模擬內容擷取與 AI 摘要生成（實際專案可在此整合 BeautifulSoup 與 Gemini API）
  mock_title = "範例文章標題：現代軟體工程實踐"
  mock_summary = (
      "- 核心概念：強調模組化與可維護性。\n- 技術選型：推薦使用 FastAPI 與"
      "輕量資料庫。\n- 開發效率：透過 MVP 快速驗證產品價值。"
  )
  mock_tags = "Python,Backend,Architecture"

  new_resource = ResourceModel(
      url=url_str,
      title=mock_title,
      summary=mock_summary,
      tags=mock_tags,
  )
  db.add(new_resource)
  db.commit()
  db.refresh(new_resource)

  return new_resource


@app.get("/api/resources", response_model=list[ResourceResponse])
def list_resources(skip: int = 0, limit: int = 10, db=Depends(get_db)):
  return (
      db.query(ResourceModel)
      .order_by(ResourceModel.created_at.desc())
      .offset(skip)
      .limit(limit)
      .all()
  )
