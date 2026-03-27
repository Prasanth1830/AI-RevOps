"""
Agent API Routes
POST /api/prospect
POST /api/deal-risk
POST /api/churn
POST /api/competitive
GET  /api/agent-runs
GET  /api/agent-runs/{run_id}
"""
from fastapi import APIRouter, HTTPException
from schemas.schemas import (
    ProspectInput, ProspectOutput,
    DealRiskInput, DealRiskOutput,
    ChurnInput, ChurnOutput,
    CompetitiveInput, CompetitiveOutput
)
from services.orchestrator import execute_agent, get_agent_run, get_recent_runs
from websocket.manager import ws_manager

router = APIRouter(prefix="/api", tags=["agents"])


@router.post("/prospect")
async def run_prospect_agent(input_data: ProspectInput):
    """Run the Prospecting Agent"""
    result = await execute_agent(
        "prospect",
        input_data.model_dump(),
        ws_manager
    )
    return result


@router.post("/deal-risk")
async def run_deal_risk_agent(input_data: DealRiskInput):
    """Run the Deal Intelligence Agent"""
    result = await execute_agent(
        "deal_risk",
        input_data.model_dump(),
        ws_manager
    )
    return result


@router.post("/churn")
async def run_churn_agent(input_data: ChurnInput):
    """Run the Revenue Retention (Churn) Agent"""
    result = await execute_agent(
        "churn",
        input_data.model_dump(),
        ws_manager
    )
    return result


@router.post("/competitive")
async def run_competitive_agent(input_data: CompetitiveInput):
    """Run the Competitive Intelligence Agent"""
    result = await execute_agent(
        "competitive",
        input_data.model_dump(),
        ws_manager
    )
    return result


@router.get("/agent-runs")
async def list_agent_runs(limit: int = 20):
    """Get recent agent runs"""
    return get_recent_runs(limit)


@router.get("/agent-runs/{run_id}")
async def get_run(run_id: int):
    """Get a specific agent run"""
    run = get_agent_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Agent run not found")
    return run
