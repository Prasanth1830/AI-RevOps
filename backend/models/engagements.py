from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from database import Base


class Engagement(Base):
    __tablename__ = "engagements"

    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    type = Column(String(50))  # email, call, meeting, demo, support
    direction = Column(String(20))  # inbound, outbound
    subject = Column(String(500))
    body = Column(Text)
    sentiment = Column(String(50))  # positive, neutral, negative
    sentiment_score = Column(Float, default=0.0)
    duration_minutes = Column(Integer, default=0)
    outcome = Column(String(100))
    logged_by = Column(String(255))
    metadata = Column(JSON, default=dict)
    engagement_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
