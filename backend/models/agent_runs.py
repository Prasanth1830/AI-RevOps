from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(Integer, primary_key=True, index=True)
    agent_type = Column(String(50), nullable=False)  # prospect, deal_risk, churn, competitive
    status = Column(String(30), default="pending")  # pending, running, completed, failed
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    execution_log = Column(JSON, default=list)
    duration_ms = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    triggered_by = Column(String(255), default="user")
    celery_task_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
