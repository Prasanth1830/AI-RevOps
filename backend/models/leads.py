from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Enum
from sqlalchemy.sql import func
from database import Base
import enum


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    LOST = "lost"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=False)
    contact_email = Column(String(255))
    contact_title = Column(String(255))
    industry = Column(String(100))
    company_size = Column(String(50))
    annual_revenue = Column(Float)
    website = Column(String(500))
    source = Column(String(100))
    status = Column(String(50), default=LeadStatus.NEW)
    lead_score = Column(Float, default=0.0)
    icp_match = Column(Float, default=0.0)
    notes = Column(Text)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
