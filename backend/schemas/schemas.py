from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============ PROSPECT AGENT ============
class ProspectInput(BaseModel):
    company_name: str = Field(..., description="Target company name")
    industry: str = Field(..., description="Company industry")
    icp_criteria: Dict[str, Any] = Field(default_factory=dict, description="Ideal Customer Profile criteria")
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    notes: Optional[str] = None


class OutreachStep(BaseModel):
    step: int
    channel: str
    timing: str
    subject: str
    message: str


class ProspectOutput(BaseModel):
    lead_score: float = Field(..., ge=0, le=100)
    score_breakdown: Dict[str, float] = Field(default_factory=dict)
    personalized_email: str
    outreach_sequence: List[OutreachStep]
    key_insights: List[str] = Field(default_factory=list)
    recommended_approach: str = ""


# ============ DEAL RISK AGENT ============
class DealRiskInput(BaseModel):
    deal_id: int
    deal_name: Optional[str] = None
    include_engagements: bool = True


class RecoveryAction(BaseModel):
    action: str
    priority: str
    talking_points: List[str]
    timeline: str


class DealRiskOutput(BaseModel):
    risk_score: float = Field(..., ge=0, le=100)
    risk_level: str  # low, medium, high, critical
    risk_reasons: List[str]
    recovery_plan: List[RecoveryAction]
    deal_health_summary: str = ""
    engagement_trend: str = ""  # improving, stable, declining


# ============ CHURN AGENT ============
class ChurnInput(BaseModel):
    account_id: int
    account_name: Optional[str] = None
    include_usage: bool = True


class InterventionRecommendation(BaseModel):
    type: str
    urgency: str
    description: str
    expected_impact: str


class ChurnOutput(BaseModel):
    churn_probability: float = Field(..., ge=0, le=100)
    risk_level: str  # low, medium, high, critical
    risk_factors: List[str]
    intervention: InterventionRecommendation
    save_email_draft: str
    health_trend: str = ""  # improving, stable, declining
    predicted_churn_window: str = ""


# ============ COMPETITIVE AGENT ============
class CompetitiveInput(BaseModel):
    deal_id: int
    competitor_names: List[str] = Field(default_factory=list)
    deal_context: Optional[str] = None


class BattlecardSection(BaseModel):
    category: str
    our_strengths: List[str]
    competitor_weaknesses: List[str]
    key_differentiators: List[str]


class CompetitiveOutput(BaseModel):
    competitor_risk_flag: str  # low, medium, high, critical
    primary_competitor: str
    battlecard: List[BattlecardSection]
    win_strategy: str
    objection_handlers: List[Dict[str, str]] = Field(default_factory=list)
    competitive_positioning: str = ""


# ============ AGENT RUN ============
class AgentRunCreate(BaseModel):
    agent_type: str
    input_data: Dict[str, Any]


class AgentRunResponse(BaseModel):
    id: int
    agent_type: str
    status: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    execution_log: List[Dict[str, Any]]
    duration_ms: int
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# ============ DASHBOARD ============
class PipelineStats(BaseModel):
    total_deals: int
    total_value: float
    avg_deal_size: float
    win_rate: float
    deals_by_stage: Dict[str, int]
    at_risk_deals: int
    pipeline_velocity: float


class DashboardSummary(BaseModel):
    pipeline: PipelineStats
    total_leads: int
    qualified_leads: int
    avg_lead_score: float
    total_accounts: int
    at_risk_accounts: int
    avg_health_score: float
    recent_agent_runs: List[AgentRunResponse]
    churn_trend: List[Dict[str, Any]]
