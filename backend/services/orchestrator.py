"""
Agent Orchestrator Service
Manages agent execution, tracks runs, handles async processing
"""
import asyncio
import time
from typing import Dict, Any, Optional
from datetime import datetime
from agents.prospect_agent import ProspectingAgent
from agents.deal_agent import DealIntelligenceAgent
from agents.churn_agent import ChurnAgent
from agents.competitive_agent import CompetitiveAgent


# In-memory store for agent runs (in production, use database)
agent_runs_store: Dict[int, Dict[str, Any]] = {}
run_counter = 0


AGENT_MAP = {
    "prospect": ProspectingAgent,
    "deal_risk": DealIntelligenceAgent,
    "churn": ChurnAgent,
    "competitive": CompetitiveAgent
}


async def execute_agent(agent_type: str, input_data: Dict[str, Any], ws_manager=None) -> Dict[str, Any]:
    """Execute an agent and track the run"""
    global run_counter
    run_counter += 1
    run_id = run_counter

    # Create run record
    run_record = {
        "id": run_id,
        "agent_type": agent_type,
        "status": "running",
        "input_data": input_data,
        "output_data": {},
        "execution_log": [],
        "duration_ms": 0,
        "error_message": None,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    agent_runs_store[run_id] = run_record

    # Notify via WebSocket
    if ws_manager:
        await ws_manager.broadcast({
            "type": "agent_status",
            "run_id": run_id,
            "agent_type": agent_type,
            "status": "running",
            "message": f"{agent_type} agent started analyzing..."
        })

    try:
        # Get agent class
        agent_class = AGENT_MAP.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")

        # Execute agent
        agent = agent_class()
        start_time = time.time()
        result = await agent.run(input_data)
        duration = int((time.time() - start_time) * 1000)

        # Update run record
        run_record["status"] = "completed"
        run_record["output_data"] = result
        run_record["execution_log"] = result.get("execution", {}).get("log", [])
        run_record["duration_ms"] = duration
        run_record["completed_at"] = datetime.now().isoformat()

        # Notify completion
        if ws_manager:
            await ws_manager.broadcast({
                "type": "agent_status",
                "run_id": run_id,
                "agent_type": agent_type,
                "status": "completed",
                "message": f"{agent_type} agent completed in {duration}ms",
                "result_preview": _get_result_preview(agent_type, result)
            })

        return {
            "run_id": run_id,
            "status": "completed",
            "result": result,
            "duration_ms": duration
        }

    except Exception as e:
        run_record["status"] = "failed"
        run_record["error_message"] = str(e)
        run_record["completed_at"] = datetime.now().isoformat()

        if ws_manager:
            await ws_manager.broadcast({
                "type": "agent_status",
                "run_id": run_id,
                "agent_type": agent_type,
                "status": "failed",
                "message": f"{agent_type} agent failed: {str(e)}"
            })

        return {
            "run_id": run_id,
            "status": "failed",
            "error": str(e)
        }


def get_agent_run(run_id: int) -> Optional[Dict[str, Any]]:
    """Get an agent run by ID"""
    return agent_runs_store.get(run_id)


def get_recent_runs(limit: int = 20) -> list:
    """Get recent agent runs"""
    runs = sorted(agent_runs_store.values(), key=lambda x: x["created_at"], reverse=True)
    return runs[:limit]


def _get_result_preview(agent_type: str, result: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a brief preview of agent results for WebSocket notification"""
    if agent_type == "prospect":
        return {
            "lead_score": result.get("lead_score"),
            "approach": result.get("recommended_approach", "")[:100]
        }
    elif agent_type == "deal_risk":
        return {
            "risk_score": result.get("risk_score"),
            "risk_level": result.get("risk_level"),
            "reasons_count": len(result.get("risk_reasons", []))
        }
    elif agent_type == "churn":
        return {
            "churn_probability": result.get("churn_probability"),
            "risk_level": result.get("risk_level"),
            "intervention_type": result.get("intervention", {}).get("type")
        }
    elif agent_type == "competitive":
        return {
            "risk_flag": result.get("competitor_risk_flag"),
            "primary_competitor": result.get("primary_competitor")
        }
    return {}
