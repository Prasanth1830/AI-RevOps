from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    industry = Column(String(100))
    company_size = Column(String(50))
    annual_revenue = Column(Float)
    website = Column(String(500))
    health_score = Column(Float, default=50.0)
    mrr = Column(Float, default=0.0)
    arr = Column(Float, default=0.0)
    contract_start = Column(DateTime(timezone=True))
    contract_end = Column(DateTime(timezone=True))
    usage_metrics = Column(JSON, default=dict)
    support_tickets_open = Column(Integer, default=0)
    support_sentiment = Column(String(50), default="neutral")
    last_engagement = Column(DateTime(timezone=True))
    churn_risk = Column(Float, default=0.0)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
