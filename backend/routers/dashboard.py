"""
Dashboard & CRM Data Routes
GET /api/dashboard
GET /api/leads
GET /api/deals
GET /api/accounts
GET /api/engagements
"""
from fastapi import APIRouter
from typing import Optional
from mock_data.generator import MOCK_DATA
from services.orchestrator import get_recent_runs
import random

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard")
async def get_dashboard():
    """Get comprehensive dashboard summary"""
    leads = MOCK_DATA["leads"]
    deals = MOCK_DATA["deals"]
    accounts = MOCK_DATA["accounts"]

    # Pipeline stats
    active_deals = [d for d in deals if d["stage"] not in ["closed_won", "closed_lost"]]
    won_deals = [d for d in deals if d["stage"] == "closed_won"]
    total_value = sum(d["amount"] for d in active_deals)
    at_risk = [d for d in active_deals if d["risk_score"] > 0.5]

    deals_by_stage = {}
    for d in deals:
        stage = d["stage"]
        deals_by_stage[stage] = deals_by_stage.get(stage, 0) + 1

    # Lead stats
    qualified = [l for l in leads if l["status"] in ["qualified", "converted"]]
    avg_score = sum(l["lead_score"] for l in leads) / max(1, len(leads))

    # Account stats
    at_risk_accounts = [a for a in accounts if a["churn_risk"] > 0.5]
    avg_health = sum(a["health_score"] for a in accounts) / max(1, len(accounts))

    # Churn trend (mock time series)
    churn_trend = []
    months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
    base_churn = 12
    for month in months:
        churn_trend.append({
            "month": month,
            "churn_rate": round(base_churn + random.uniform(-3, 5), 1),
            "accounts_churned": random.randint(0, 4),
            "mrr_lost": round(random.uniform(1000, 15000), 2)
        })
        base_churn += random.uniform(-2, 2)

    # Pipeline health trend
    pipeline_health = []
    for month in months:
        pipeline_health.append({
            "month": month,
            "total_value": round(random.uniform(200000, 800000), 0),
            "new_deals": random.randint(2, 8),
            "won_deals": random.randint(0, 4),
            "lost_deals": random.randint(0, 3)
        })

    return {
        "pipeline": {
            "total_deals": len(deals),
            "active_deals": len(active_deals),
            "total_value": round(total_value, 2),
            "avg_deal_size": round(total_value / max(1, len(active_deals)), 2),
            "win_rate": round(len(won_deals) / max(1, len(deals)) * 100, 1),
            "deals_by_stage": deals_by_stage,
            "at_risk_deals": len(at_risk),
            "pipeline_velocity": round(random.uniform(15, 45), 1)
        },
        "leads": {
            "total": len(leads),
            "qualified": len(qualified),
            "avg_score": round(avg_score, 1),
            "conversion_rate": round(len([l for l in leads if l["status"] == "converted"]) / max(1, len(leads)) * 100, 1)
        },
        "accounts": {
            "total": len(accounts),
            "at_risk": len(at_risk_accounts),
            "avg_health_score": round(avg_health, 1),
            "total_arr": round(sum(a["arr"] for a in accounts), 2),
            "total_mrr": round(sum(a["mrr"] for a in accounts), 2)
        },
        "recent_agent_runs": get_recent_runs(5),
        "churn_trend": churn_trend,
        "pipeline_health": pipeline_health
    }


@router.get("/leads")
async def get_leads(
    status: Optional[str] = None,
    industry: Optional[str] = None,
    min_score: Optional[float] = None
):
    """Get all leads with optional filters"""
    leads = MOCK_DATA["leads"]

    if status:
        leads = [l for l in leads if l["status"] == status]
    if industry:
        leads = [l for l in leads if l["industry"] == industry]
    if min_score is not None:
        leads = [l for l in leads if l["lead_score"] >= min_score]

    return {"count": len(leads), "leads": leads}


@router.get("/deals")
async def get_deals(stage: Optional[str] = None):
    """Get all deals with optional stage filter"""
    deals = MOCK_DATA["deals"]

    if stage:
        deals = [d for d in deals if d["stage"] == stage]

    return {"count": len(deals), "deals": deals}


@router.get("/deals/{deal_id}")
async def get_deal(deal_id: int):
    """Get a specific deal with engagements"""
    from tools.crm_tools import get_deal_data
    return get_deal_data(deal_id)


@router.get("/accounts")
async def get_accounts():
    """Get all accounts"""
    accounts = MOCK_DATA["accounts"]
    return {"count": len(accounts), "accounts": accounts}


@router.get("/accounts/{account_id}")
async def get_account(account_id: int):
    """Get a specific account with details"""
    from tools.crm_tools import get_account_data
    return get_account_data(account_id)


@router.get("/engagements")
async def get_engagements(deal_id: Optional[int] = None, account_id: Optional[int] = None):
    """Get engagements with optional filters"""
    engagements = MOCK_DATA["engagements"]

    if deal_id:
        engagements = [e for e in engagements if e["deal_id"] == deal_id]
    if account_id:
        engagements = [e for e in engagements if e.get("account_id") == account_id]

    return {"count": len(engagements), "engagements": engagements}
