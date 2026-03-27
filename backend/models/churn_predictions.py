from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from database import Base


class ChurnPrediction(Base):
    __tablename__ = "churn_predictions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    churn_probability = Column(Float, default=0.0)
    risk_level = Column(String(20))  # low, medium, high, critical
    risk_factors = Column(JSON, default=list)
    intervention_type = Column(String(100))
    intervention_details = Column(JSON, default=dict)
    save_email_draft = Column(Text)
    predicted_churn_date = Column(DateTime(timezone=True), nullable=True)
    agent_run_id = Column(Integer, ForeignKey("agent_runs.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
