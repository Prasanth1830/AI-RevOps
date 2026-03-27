from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from database import Base
import enum


class DealStage(str, enum.Enum):
    DISCOVERY = "discovery"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    deal_name = Column(String(255), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    owner = Column(String(255))
    stage = Column(String(50), default=DealStage.DISCOVERY)
    amount = Column(Float, default=0.0)
    probability = Column(Float, default=0.0)
    expected_close_date = Column(DateTime(timezone=True))
    actual_close_date = Column(DateTime(timezone=True), nullable=True)
    risk_score = Column(Float, default=0.0)
    risk_reasons = Column(JSON, default=list)
    competitor_mentions = Column(JSON, default=list)
    next_steps = Column(Text)
    notes = Column(Text)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
